// Simulador offline de uma tela Power Apps (Canvas):
// avalia as fórmulas REAIS dos controles (Controls/<n>.json) com o interpretador
// oficial Microsoft.PowerFx sobre dados de teste e exporta a árvore renderizável.
// Uso: screensim <controls.json> <cenario.json> <saida.json>
using System.Globalization;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.PowerFx;
using Microsoft.PowerFx.Types;

var ctrlDoc = JsonDocument.Parse(File.ReadAllText(args[0]));
var scen = JsonDocument.Parse(File.ReadAllText(args[1])).RootElement;
var sim = new Sim(ctrlDoc.RootElement.GetProperty("TopParent"), scen);
var output = sim.Run();
File.WriteAllText(args[2], JsonSerializer.Serialize(output, new JsonSerializerOptions { WriteIndented = false }));
Console.WriteLine($"avaliações: {sim.EvalCount}  avisos: {sim.Warnings.Count}");
foreach (var w in sim.Warnings.Distinct().Take(60)) Console.WriteLine("AVISO " + w);

class Ctrl
{
    public string Name = "", Template = "";
    public Dictionary<string, string> Rules = new();
    public List<Ctrl> Children = new();
    public Ctrl? Parent;
    public Ctrl? Gallery; // galeria que contém o controle (template)
}

class Ctx
{
    public RecordValue? Item; public int Index = -1; public Ctrl? Gallery;
    public string Key => Gallery == null ? "-" : Gallery.Name + "#" + Index;
}

class NotifyFunction : ReflectionFunction
{
    public NotifyFunction() : base("Notify", FormulaType.String, FormulaType.String, FormulaType.String) { }
    public StringValue Execute(StringValue m, StringValue t) => FormulaValue.New(m.Value + " [" + t.Value + "]");
}

class Sim
{
    public int EvalCount; public List<string> Warnings = new();
    readonly Ctrl root; readonly Dictionary<string, Ctrl> byName = new();
    readonly RecalcEngine engine; readonly ParserOptions opts;
    readonly Dictionary<string, FormulaValue> globals = new();
    readonly Dictionary<string, FormulaValue> memo = new();
    readonly HashSet<string> stack = new();
    readonly JsonElement scen; readonly double W, H;
    readonly Dictionary<string, string> inputs = new();
    static readonly Regex EnumRx = new(@"\b(DisplayMode|FontWeight|NotificationType|TextMode|Align|VerticalAlign|ImagePosition|BorderStyle|Icon|DropShadow|LayoutMode|LayoutDirection|LayoutAlignItems|LayoutJustifyContent|LayoutOverflow|ScreenTransition|Transition|LoadingSpinner|Layout|Direction|TextFormat|Overflow|PenMode|TeamsTheme)\.([A-Za-z0-9_]+)");
    static readonly Regex FontRx = new(@"\bFont\.'[^']*'|\bFont\.[A-Za-z]+");
    static readonly Regex ThemeRx = new(@"\bApp\.Theme\.[A-Za-z0-9_.]+");
    static readonly Regex RefRx = new(@"\b([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)");

    public Sim(JsonElement top, JsonElement scenario)
    {
        scen = scenario;
        W = scen.GetProperty("screenW").GetDouble(); H = scen.GetProperty("screenH").GetDouble();
        root = Load(top, null, null);
        var config = new PowerFxConfig(Features.PowerFxV1);
#pragma warning disable CS0618
        config.EnableParseJSONFunction();
#pragma warning restore CS0618
        config.EnableRegExFunctions();
        config.AddFunction(new NotifyFunction());
        config.MaxCallDepth = 2000;
        engine = new RecalcEngine(config);
        opts = new ParserOptions { Culture = CultureInfo.InvariantCulture, AllowsSideEffects = true };
        if (scen.TryGetProperty("inputs", out var inp))
            foreach (var p in inp.EnumerateObject()) inputs[p.Name] = p.Value.GetString() ?? "";
        var dateFields = new HashSet<string>(scen.GetProperty("dateFields").EnumerateArray().Select(e => e.GetString()!));
        foreach (var g in scen.GetProperty("globals").EnumerateObject())
            globals[g.Name] = Conv.From(g.Value, dateFields, g.Name);
        // coleções/variáveis derivadas (mesmas fórmulas do app)
        if (scen.TryGetProperty("derive", out var der))
            foreach (var d in der.EnumerateArray())
            {
                var name = d.GetProperty("name").GetString()!;
                string expr = d.TryGetProperty("fromOnVisible", out var ov)
                    ? ExtractClearCollect(root.Rules["OnVisible"], ov.GetString()!)
                    : d.GetProperty("expr").GetString()!;
                globals[name] = EvalText(expr, null, null, "derive:" + name);
            }
    }

    Ctrl Load(JsonElement e, Ctrl? parent, Ctrl? gallery)
    {
        var c = new Ctrl { Name = e.GetProperty("Name").GetString()!, Template = e.GetProperty("Template").GetProperty("Name").GetString()!, Parent = parent, Gallery = gallery };
        foreach (var r in e.GetProperty("Rules").EnumerateArray())
            c.Rules[r.GetProperty("Property").GetString()!] = r.GetProperty("InvariantScript").GetString()!;
        byName[c.Name] = c;
        var g = c.Template == "gallery" ? c : gallery;
        foreach (var ch in e.GetProperty("Children").EnumerateArray())
        {
            var cc = Load(ch, c, g);
            if (cc.Template != "galleryTemplate") c.Children.Add(cc);
        }
        return c;
    }

    static string ExtractClearCollect(string onVisible, string coll)
    {
        int i = onVisible.IndexOf("ClearCollect(" + coll + ",", StringComparison.Ordinal);
        if (i < 0) throw new Exception("ClearCollect não encontrado: " + coll);
        int start = i + ("ClearCollect(" + coll + ",").Length, depth = 1; bool str = false;
        for (int k = start; k < onVisible.Length; k++)
        {
            char ch = onVisible[k];
            if (ch == '"') { str = !str; continue; }
            if (str) continue;
            if (ch == '(') depth++;
            else if (ch == ')') { depth--; if (depth == 0) return onVisible.Substring(start, k - start); }
        }
        throw new Exception("parênteses");
    }

    // ------------------------------------------------------------------ reescrita
    // Fora de literais de texto: Self/Parent/ThisItem -> zSelf/zParent/zThisItem; enums de UI -> texto.
    static string Rewrite(string f)
    {
        var sb = new System.Text.StringBuilder(); int i = 0;
        while (i < f.Length)
        {
            if (f[i] == '"')
            {
                int j = i + 1;
                while (j < f.Length) { if (f[j] == '"') { if (j + 1 < f.Length && f[j + 1] == '"') { j += 2; continue; } break; } j++; }
                sb.Append(f, i, Math.Min(j + 1, f.Length) - i); i = j + 1; continue;
            }
            int k = f.IndexOf('"', i); if (k < 0) k = f.Length;
            var code = f.Substring(i, k - i);
            code = Regex.Replace(code, @"\bSelf\.", "zSelf.");
            code = Regex.Replace(code, @"\bParent\.", "zParent.");
            code = Regex.Replace(code, @"\bThisItem\b", "zThisItem");
            code = Regex.Replace(code, @"\bUser\(\)", "{FullName: \"\", Email: \"\"}");
            code = Regex.Replace(code, @"\bApp\.(Width|Height)\b", "1366");
            code = FontRx.Replace(code, "\"font\"");
            code = ThemeRx.Replace(code, "RGBA(0, 0, 0, 0)");
            code = EnumRx.Replace(code, m => "\"" + m.Groups[1].Value + "." + m.Groups[2].Value + "\"");
            sb.Append(code); i = k;
        }
        return sb.ToString();
    }

    static IEnumerable<(string obj, string prop)> Refs(string f)
    {
        // somente trechos de código (fora de literais)
        var code = Regex.Replace(f, "\"(?:[^\"]|\"\")*\"", "\"\"");
        foreach (Match m in RefRx.Matches(code)) yield return (m.Groups[1].Value, m.Groups[2].Value);
    }

    // ------------------------------------------------------------------ avaliação
    static readonly Dictionary<string, string> Defaults = new()
    {
        ["Visible"] = "true", ["X"] = "0", ["Y"] = "0", ["Width"] = "0", ["Height"] = "0", ["WrapCount"] = "1",
        ["TemplatePadding"] = "0", ["BorderThickness"] = "0", ["PaddingTop"] = "0", ["PaddingBottom"] = "0",
        ["PaddingLeft"] = "0", ["PaddingRight"] = "0", ["Size"] = "13", ["DisplayMode"] = "\"DisplayMode.Edit\"",
        ["Tooltip"] = "\"\"", ["HintText"] = "\"\"", ["Default"] = "\"\"", ["Text"] = "\"\"",
    };

    public FormulaValue Prop(Ctrl c, string prop, Ctx? ctx)
    {
        // propriedades sintéticas
        if (c.Template == "screen" && (prop == "Width" || prop == "Height")) return FormulaValue.New(prop == "Width" ? W : H);
        if (c.Template == "gallery" && prop == "TemplateHeight") return Prop(c, "TemplateSize", null);
        if (c.Template == "gallery" && prop == "TemplateWidth")
        {
            var w = Num(Prop(c, "Width", null)); var wc = Math.Max(1, Num(Prop(c, "WrapCount", null)));
            return FormulaValue.New(Math.Floor(w / wc));
        }
        if (c.Template == "text" && prop == "Text")
            return FormulaValue.New(inputs.TryGetValue(c.Name, out var t) ? t : Str(Prop(c, "Default", ctx)));
        if (c.Gallery == null) ctx = null; // fora de galeria não há ThisItem
        var key = c.Name + "|" + prop + "|" + (ctx?.Key ?? "-");
        if (memo.TryGetValue(key, out var v)) return v;
        if (!stack.Add(key)) { Warnings.Add("ciclo " + key); return FormulaValue.NewBlank(); }
        try
        {
            string? f = c.Rules.TryGetValue(prop, out var rf) ? rf : (Defaults.TryGetValue(prop, out var df) ? df : null);
            v = f == null ? FormulaValue.NewBlank() : EvalText(f, c, ctx, c.Name + "." + prop);
            memo[key] = v; return v;
        }
        finally { stack.Remove(key); }
    }

    FormulaValue EvalText(string formula, Ctrl? self, Ctx? ctx, string label)
    {
        EvalCount++;
        var f = Rewrite(formula);
        var fields = new Dictionary<string, FormulaValue>(globals);
        var need = new Dictionary<string, Dictionary<string, FormulaValue>>();
        foreach (var (obj, prop) in Refs(f))
        {
            Ctrl? target = null; Ctx? tctx = null;
            if (obj == "zSelf" && self != null) { target = self; tctx = ctx; }
            else if (obj == "zParent" && self != null)
            {
                target = self.Parent; tctx = ctx;
                if (target != null && target.Template == "gallery" && self.Gallery == target) tctx = null;
            }
            else if (byName.TryGetValue(obj, out var named) && !globals.ContainsKey(obj))
            {
                target = named;
                tctx = named.Gallery != null && ctx?.Gallery == named.Gallery ? ctx : null;
            }
            if (target == null) continue;
            if (!need.TryGetValue(obj, out var d)) need[obj] = d = new();
            if (!d.ContainsKey(prop)) d[prop] = target.Gallery != null && tctx == null && target.Template != "gallery" ? FormulaValue.NewBlank() : Prop(target, prop, tctx);
        }
        foreach (var (obj, d) in need)
            fields[obj] = RecordValue.NewRecordFromFields(d.Select(kv => new NamedValue(kv.Key, kv.Value)));
        if (ctx?.Item != null) fields["zThisItem"] = ctx.Item;
        var rec = RecordValue.NewRecordFromFields(fields.Select(kv => new NamedValue(kv.Key, kv.Value)));
        try
        {
            var r = engine.Eval(f, rec, opts);
            if (r is ErrorValue ev) { Warnings.Add(label + ": " + string.Join("; ", ev.Errors.Select(e => e.Message))); return FormulaValue.NewBlank(); }
            return r;
        }
        catch (Exception ex) { Warnings.Add(label + ": " + ex.Message.Split('\n')[0]); return FormulaValue.NewBlank(); }
    }

    static double Num(FormulaValue v) => v is NumberValue n ? n.Value : v is DecimalValue d ? (double)d.Value : 0;
    static string Str(FormulaValue v) => v switch { StringValue s => s.Value, NumberValue n => n.Value.ToString(CultureInfo.InvariantCulture), BlankValue => "", BooleanValue b => b.Value ? "true" : "false", _ => v.ToObject()?.ToString() ?? "" };
    static bool Bool(FormulaValue v) => v is BooleanValue b ? b.Value : !(v is BlankValue);
    static string? Color(FormulaValue v) => v is ColorValue c ? $"rgba({c.Value.R},{c.Value.G},{c.Value.B},{(c.Value.A / 255.0).ToString("0.###", CultureInfo.InvariantCulture)})" : null;

    // ------------------------------------------------------------------ árvore de saída
    static readonly string[] NumProps = { "X", "Y", "Width", "Height", "Size", "BorderThickness", "RadiusTopLeft", "RadiusTopRight", "RadiusBottomLeft", "RadiusBottomRight", "PaddingTop", "PaddingBottom", "PaddingLeft", "PaddingRight", "ZIndex", "TemplateSize", "WrapCount" };
    static readonly string[] ColorProps = { "Fill", "Color", "BorderColor", "DisabledFill", "DisabledColor", "DisabledBorderColor" };
    static readonly string[] TextProps = { "HtmlText", "Text", "HintText", "Tooltip", "DisplayMode", "FontWeight", "Icon", "Image", "ImagePosition", "Align", "Underline" };

    Dictionary<string, object?> Node(Ctrl c, Ctx? ctx)
    {
        var n = new Dictionary<string, object?> { ["name"] = c.Name, ["type"] = c.Template };
        var vis = Bool(Prop(c, "Visible", ctx));
        n["visible"] = vis;
        if (!vis && c.Template != "screen") return n;
        foreach (var p in NumProps) if (c.Rules.ContainsKey(p) || p is "X" or "Y" or "Width" or "Height") n[p] = Num(Prop(c, p, ctx));
        foreach (var p in ColorProps) if (c.Rules.ContainsKey(p)) n[p] = Color(Prop(c, p, ctx));
        foreach (var p in TextProps) if (c.Rules.ContainsKey(p)) n[p] = Str(Prop(c, p, ctx));
        if (c.Template == "text") { n["Text"] = Str(Prop(c, "Text", ctx)); }
        if (c.Template == "gallery")
        {
            var items = Prop(c, "Items", ctx) as TableValue;
            var list = new List<object>();
            int idx = 0;
            if (items != null)
                foreach (var row in items.Rows.Take(40))
                {
                    var ictx = new Ctx { Item = row.Value, Index = idx, Gallery = c };
                    list.Add(new Dictionary<string, object?> { ["index"] = idx, ["children"] = c.Children.Select(ch => Node(ch, ictx)).ToList() });
                    idx++;
                }
            n["TemplateWidth"] = Num(Prop(c, "TemplateWidth", null));
            n["TemplateHeight"] = Num(Prop(c, "TemplateHeight", null));
            n["items"] = list;
            n["count"] = items?.Rows.Count() ?? 0;
        }
        else n["children"] = c.Children.Select(ch => Node(ch, ctx)).ToList();
        return n;
    }

    public object Run()
    {
        var tree = Node(root, null);
        var probes = new Dictionary<string, object?>();
        if (scen.TryGetProperty("probes", out var pr))
            foreach (var p in pr.EnumerateArray())
            {
                var name = p.GetProperty("name").GetString()!;
                FormulaValue v;
                if (p.TryGetProperty("control", out var ctl))
                    v = Prop(byName[ctl.GetString()!], p.GetProperty("prop").GetString()!, null);
                else v = EvalText(p.GetProperty("expr").GetString()!, root, null, "probe:" + name);
                probes[name] = Str(v);
            }
        return new Dictionary<string, object?> { ["tree"] = tree, ["probes"] = probes, ["warnings"] = Warnings.Distinct().ToList() };
    }
}

static class Conv
{
    static readonly Regex Iso = new(@"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?)?");

    public static FormulaValue From(JsonElement e, HashSet<string> dateFields, string field)
    {
        switch (e.ValueKind)
        {
            case JsonValueKind.Object:
                return RecordValue.NewRecordFromFields(e.EnumerateObject().Select(p => new NamedValue(p.Name, From(p.Value, dateFields, p.Name))));
            case JsonValueKind.Array:
                return Table(e, dateFields);
            case JsonValueKind.String:
                var s = e.GetString()!;
                if (dateFields.Contains(field) && Iso.IsMatch(s)) return FormulaValue.New(DateTime.Parse(s, CultureInfo.InvariantCulture));
                return FormulaValue.New(s);
            case JsonValueKind.Number: return FormulaValue.New(e.GetDouble());
            case JsonValueKind.True: return FormulaValue.New(true);
            case JsonValueKind.False: return FormulaValue.New(false);
            default: return FormulaValue.NewBlank();
        }
    }

    static FormulaType TypeOf(JsonElement e, HashSet<string> dateFields, string field) => e.ValueKind switch
    {
        JsonValueKind.String => dateFields.Contains(field) ? FormulaType.DateTime : FormulaType.String,
        JsonValueKind.Number => FormulaType.Number,
        JsonValueKind.True or JsonValueKind.False => FormulaType.Boolean,
        _ => FormulaType.String,
    };

    // tabela com esquema uniforme (campos nulos tipados como em outras linhas)
    static TableValue Table(JsonElement arr, HashSet<string> dateFields)
    {
        var rows = arr.EnumerateArray().ToList();
        if (rows.Count > 0 && rows[0].ValueKind != JsonValueKind.Object)
            return FormulaValue.NewSingleColumnTable(rows.Select(r => (FormulaValue)From(r, dateFields, "Value")).Cast<FormulaValue>().Select(v => (StringValue)v));
        var schema = new Dictionary<string, FormulaType>();
        foreach (var r in rows) foreach (var p in r.EnumerateObject())
                if (!schema.ContainsKey(p.Name) && p.Value.ValueKind != JsonValueKind.Null) schema[p.Name] = TypeOf(p.Value, dateFields, p.Name);
        foreach (var r in rows) foreach (var p in r.EnumerateObject()) if (!schema.ContainsKey(p.Name)) schema[p.Name] = FormulaType.String;
        var rt = RecordType.Empty();
        foreach (var kv in schema) rt = rt.Add(kv.Key, kv.Value);
        var recs = rows.Select(r =>
        {
            var vals = new List<NamedValue>();
            foreach (var kv in schema)
            {
                FormulaValue v = r.TryGetProperty(kv.Key, out var pv) && pv.ValueKind != JsonValueKind.Null ? From(pv, dateFields, kv.Key) : FormulaValue.NewBlank(kv.Value);
                vals.Add(new NamedValue(kv.Key, v));
            }
            return RecordValue.NewRecordFromFields(rt, vals);
        }).ToList();
        return FormulaValue.NewTable(rt, recs);
    }
}

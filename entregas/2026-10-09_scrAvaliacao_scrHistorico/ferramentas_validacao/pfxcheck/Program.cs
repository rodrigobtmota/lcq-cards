using System.Globalization;
using System.Text.Json;
using Microsoft.PowerFx;
// Lê um arquivo JSON [{id, formula}] e reporta erros de sintaxe (parse) por fórmula.
var items = JsonSerializer.Deserialize<List<Dictionary<string,string>>>(File.ReadAllText(args[0]))!;
var engine = new Engine(new PowerFxConfig());
var culture = args.Length > 1 ? new CultureInfo(args[1]) : CultureInfo.InvariantCulture;
var opts = new ParserOptions { AllowsSideEffects = true, Culture = culture };
int ok = 0, bad = 0;
foreach (var it in items) {
    var r = engine.Parse(it["formula"], opts);
    if (r.IsSuccess) { ok++; continue; }
    bad++;
    foreach (var e in r.Errors) Console.WriteLine($"ERRO\t{it["id"]}\t{e.Message}\t{e.Span?.Min}");
}
Console.WriteLine($"TOTAL\t{items.Count}\tOK\t{ok}\tFALHA\t{bad}");

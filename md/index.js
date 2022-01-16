const path = require("path");
const mume = require("@shd101wyy/mume");

async function main() {
  const configPath = path.resolve(".mume");
  await mume.init(configPath);

  const engine = new mume.MarkdownEngine({
    filePath: "./index.md",
    config: {
      configPath: configPath,
      previewTheme: "github-light.css",
      // revealjsTheme: "white.css"
      codeBlockTheme: "default.css",
      printBackground: true,
      enableScriptExecution: true, // <= for running code chunks
    },
  });

  // html export
  await engine.htmlExport({ offline: false, runAllCodeChunks: true });
  return process.exit();
}

main();

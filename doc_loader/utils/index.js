import fs from "fs";
import path from "path";
import { writeFile } from "fs/promises";

const absolutePath = path.resolve("../files");

const markdownFiles = [];

function findMarkdownFiles(directory) {
  fs.readdirSync(directory).forEach((file) => {
    const fullPath = path.join(directory, file);
    if (fs.statSync(fullPath).isDirectory()) {
      findMarkdownFiles(fullPath);
    } else if (path.extname(fullPath).toLowerCase() === ".mdx") {
      markdownFiles.push(fullPath);
    }
  });
}

findMarkdownFiles(absolutePath);
console.log(markdownFiles);

async function removeImportsFromMarkdown(markdownFile) {
  const content = fs.readFileSync(markdownFile, 'utf-8');
  const lines = content.split('\n');

  const modifiedLines = lines.filter(line => {
    return !line.includes('@site')
     && !line.includes('<ResponsiveVideo') 
     && !line.includes('</Subhead') 
     && !line.includes('<Subhead') 
     && !line.includes('<HomepageFeatures')
  });

  fs.writeFileSync(markdownFile, modifiedLines.join('\n'), 'utf-8');
  const markdown = fs.readFileSync(markdownFile, 'utf-8');
  return markdown;
}

export async function mdxToMarkdown(markdownFiles) {
  // TODO mdx to md
  for (let i = 0; i < markdownFiles.length; i++) {
    const newName = markdownFiles[i].replace(".mdx", ".md");
    const markdown = await removeImportsFromMarkdown(markdownFiles[i]);

    await writeFile(`${newName}`, markdown)
  }
}

mdxToMarkdown(markdownFiles);

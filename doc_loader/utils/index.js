import { mdxToMd } from "mdx-to-md";
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

export async function mdxToMarkdown(markdownFiles) {
  // TODO mdx to md
  for (let i = 0; i < markdownFiles.length; i++) {
    const fileName = path.basename(markdownFiles[i], ".mdx");
    const newName = markdownFiles[i].replace(".mdx", ".md");
    console.log(fileName);
    const markdown = await mdxToMd(markdownFiles[i]);
    await writeFile(`${newName}`, markdown)
    console.log(markdown);
  }
}

mdxToMarkdown(markdownFiles);

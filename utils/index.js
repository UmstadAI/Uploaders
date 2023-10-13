import { mdxToMd } from "mdx-to-md"
import fs from "fs"
import path from "path";

const basePath = "../doc_loader/files"

const markdownFiles = [];

function findMarkdownFiles(directory) {

    fs.readdirSync(directory).forEach(file => {
        const fullPath = path.join(directory, file);
        if (fs.statSync(fullPath).isDirectory()) {
            findMarkdownFiles(fullPath);
        } else if (path.extname(fullPath).toLowerCase() === '.mdx') {
            markdownFiles.push(fullPath);
        }
    });
}

findMarkdownFiles(basePath);
console.log(markdownFiles)

export async function mdxToMarkdown(markdownFiles) {
    // TODO mdx to md
}

mdxToMarkdown(markdownFiles)
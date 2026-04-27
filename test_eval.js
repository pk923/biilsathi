const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const html = fs.readFileSync('templates.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });
setTimeout(() => {
    console.log("IFRAME CONTENT:", dom.window.document.querySelector('iframe').contentDocument.body.innerHTML.substring(0, 500));
}, 1000);

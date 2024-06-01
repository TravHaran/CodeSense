const esprima = require('esprima');
const fs = require('fs');

function extractCallHierarchy(sourceCode) {
    const ast = esprima.parseScript(sourceCode, { range: true });
    const callHierarchy = {};
    let currentFunction = null;

    function traverse(node) {
        switch (node.type) {
            case 'FunctionDeclaration':
                currentFunction = node.id.name;
                if (!callHierarchy[currentFunction]) {
                    callHierarchy[currentFunction] = [];
                }
                node.body.body.forEach(traverse);
                currentFunction = null;
                break;
            case 'ExpressionStatement':
                traverse(node.expression);
                break;
            case 'CallExpression':
                if (node.callee.type === 'Identifier' && currentFunction) {
                    callHierarchy[currentFunction].push({
                        function_name: node.callee.name,
                        code_snippet: sourceCode.slice(node.range[0], node.range[1])
                    });
                }
                break;
            default:
                if (node.body && Array.isArray(node.body)) {
                    node.body.forEach(traverse);
                }
                break;
        }
    }

    traverse(ast);
    return callHierarchy;
}

function saveAsJson(data, filename) {
    fs.writeFileSync(filename, JSON.stringify(data, null, 4));
}

const sourceCode = `
function foo() {
    bar();
}

function bar() {
    baz();
}

function baz() {
    console.log('baz');
}
`;

const callHierarchy = extractCallHierarchy(sourceCode);
saveAsJson(callHierarchy, 'call_hierarchy.json');

console.log("Call hierarchy saved to 'call_hierarchy.json'");

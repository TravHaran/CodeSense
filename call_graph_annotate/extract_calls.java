import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class JavaCallHierarchyExtractor {

    public static void main(String[] args) {
        // Example source code as a string
        String sourceCode = """
            public class Example {
                public void foo() {
                    bar();
                }

                public void bar() {
                    baz();
                }

                public void baz() {
                    System.out.println("baz");
                }
            }
            """;

        try {
            Map<String, List<Map<String, String>>> callHierarchy = extractCallHierarchy(sourceCode);
            saveAsJson(callHierarchy, "call_hierarchy.json");
            System.out.println("Call hierarchy saved to 'call_hierarchy.json'");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static Map<String, List<Map<String, String>>> extractCallHierarchy(String sourceCode) throws IOException {
        CompilationUnit compilationUnit = JavaParser.parse(sourceCode);
        CallHierarchyVisitor visitor = new CallHierarchyVisitor(sourceCode);
        visitor.visit(compilationUnit, null);
        return visitor.getCallHierarchy();
    }

    private static void saveAsJson(Map<String, List<Map<String, String>>> data, String filename) {
        try (FileWriter file = new FileWriter(filename)) {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            gson.toJson(data, file);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class CallHierarchyVisitor extends VoidVisitorAdapter<Void> {
        private final Map<String, List<Map<String, String>>> callHierarchy = new HashMap<>();
        private final String sourceCode;
        private String currentMethod = null;

        public CallHierarchyVisitor(String sourceCode) {
            this.sourceCode = sourceCode;
        }

        @Override
        public void visit(MethodDeclaration md, Void arg) {
            currentMethod = md.getNameAsString();
            callHierarchy.putIfAbsent(currentMethod, new ArrayList<>());
            super.visit(md, arg);
            currentMethod = null;
        }

        @Override
        public void visit(MethodCallExpr mc, Void arg) {
            if (currentMethod != null) {
                String calledMethod = mc.getNameAsString();
                String codeSnippet = mc.toString();
                Map<String, String> callInfo = new HashMap<>();
                callInfo.put("function_name", calledMethod);
                callInfo.put("code_snippet", codeSnippet);
                callHierarchy.get(currentMethod).add(callInfo);
            }
            super.visit(mc, arg);
        }

        public Map<String, List<Map<String, String>>> getCallHierarchy() {
            return callHierarchy;
        }
    }
}

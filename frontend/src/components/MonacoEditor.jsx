import Editor from '@monaco-editor/react';

export default function MonacoEditor({ value, onChange, language, readOnly = false, height = "100%" }) {
    return (
        <Editor
            height={height}
            language={language}
            value={value}
            theme="vs-dark"
            onChange={onChange}
            options={{
                readOnly: readOnly,
                fontSize: 14,
                minimap: { enabled: false },
                automaticLayout: true,
                wordWrap: "on",
                lineNumbers: "on",
                scrollBeyondLastLine: false,
            }}
        />
    );
}

import sys

PROBLEMS_DATA = [
    {
        "id": "P001",
        "title": "Two Sum",
        "difficulty": "easy",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists.",
        "time_limit_seconds": 5,
        "tags": ["array", "hash-table"],
        "examples": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"}
        ],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nums = ast.literal_eval(lines[0])\n    target = int(lines[1])\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split('\\n');\n    const nums = JSON.parse(lines[0]);\n    const target = parseInt(lines[1]);\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[2,7,11,15]\n9", "expected": "[0,1]", "description": "Basic case"},
            {"input": "[3,2,4]\n6", "expected": "[1,2]", "description": "Elements not at start"}
        ],
        "hidden_test_cases": [
            {"input": "[3,3]\n6", "expected": "[0,1]"},
            {"input": "[2,5,5,11]\n10", "expected": "[1,2]"},
            {"input": "[-1,-2,-3,-4,-5]\n-8", "expected": "[2,4]"}
        ]
    },
    {
        "id": "P002",
        "title": "Reverse String",
        "difficulty": "easy",
        "description": "Write a function that reverses a string.",
        "constraints": "1 <= s.length <= 10^5\ns consists of printable ascii characters.",
        "time_limit_seconds": 5,
        "tags": ["string"],
        "examples": [
            {"input": "hello", "output": "olleh"}
        ],
        "starter_code": {
            "python": "def solve(input_data):\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        if(scanner.hasNextLine()) {\n            String s = scanner.nextLine();\n            // Write your solution here\n        }\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "hello", "expected": "olleh", "description": "Basic lowercase"},
            {"input": "Hannah", "expected": "hannaH", "description": "Mixed case palindrome"}
        ],
        "hidden_test_cases": [
            {"input": "12345", "expected": "54321"},
            {"input": "  a  ", "expected": "  a  "},
            {"input": "A", "expected": "A"}
        ]
    },
    {
        "id": "P003",
        "title": "FizzBuzz",
        "difficulty": "easy",
        "description": "Given an integer n, return a string array answer (1-indexed) where:\nanswer[i] == \"FizzBuzz\" if i is divisible by 3 and 5.\nanswer[i] == \"Fizz\" if i is divisible by 3.\nanswer[i] == \"Buzz\" if i is divisible by 5.\nanswer[i] == i (as a string) if none of the above conditions are true.",
        "constraints": "1 <= n <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["math", "simulation"],
        "examples": [
            {"input": "3", "output": "[\"1\",\"2\",\"Fizz\"]"}
        ],
        "starter_code": {
            "python": "def solve(input_data):\n    n = int(input_data)\n    # Return a list of strings\n    pass",
            "javascript": "function solve(n) {\n    // n is already parsed if needed, or parse from input\n    const data = parseInt(n);\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        int n = scanner.nextInt();\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "3", "expected": "[\"1\",\"2\",\"Fizz\"]", "description": "Up to 3"},
            {"input": "5", "expected": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]", "description": "Up to 5"}
        ],
        "hidden_test_cases": [
            {"input": "15", "expected": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\",\"Fizz\",\"7\",\"8\",\"Fizz\",\"Buzz\",\"11\",\"Fizz\",\"13\",\"14\",\"FizzBuzz\"]"},
            {"input": "1", "expected": "[\"1\"]"},
            {"input": "2", "expected": "[\"1\",\"2\"]"}
        ]
    },
    {
        "id": "P004",
        "title": "Palindrome Check",
        "difficulty": "easy",
        "description": "Given a string s, return true if it is a palindrome, or false otherwise.",
        "constraints": "1 <= s.length <= 10^5\ns consists only of printable ASCII characters.",
        "time_limit_seconds": 5,
        "tags": ["string"],
        "examples": [
            {"input": "racecar", "output": "true"}
        ],
        "starter_code": {
            "python": "def solve(input_data):\n    # Return True or False\n    pass",
            "javascript": "function solve(s) {\n    // Return true or false\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        if(scanner.hasNextLine()) {\n            String s = scanner.nextLine();\n            // Write your solution here\n        }\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "racecar", "expected": "true", "description": "Simple palindrome"},
            {"input": "hello", "expected": "false", "description": "Not a palindrome"}
        ],
        "hidden_test_cases": [
            {"input": "a", "expected": "true"},
            {"input": "ab", "expected": "false"},
            {"input": "aabbccbbaa", "expected": "true"}
        ]
    },
    {
        "id": "P005",
        "title": "Find Maximum",
        "difficulty": "easy",
        "description": "Given an array of numbers, find the maximum value.",
        "constraints": "1 <= nums.length <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["array"],
        "examples": [
            {"input": "[1,2,3]", "output": "3"}
        ],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    nums = ast.literal_eval(input_data)\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const nums = JSON.parse(data);\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,2,3]", "expected": "3", "description": "Increasing"},
            {"input": "[-1,-5,-2]", "expected": "-1", "description": "Negative"}
        ],
        "hidden_test_cases": [
            {"input": "[100]", "expected": "100"},
            {"input": "[5,5,5]", "expected": "5"},
            {"input": "[10,20,30,5,1]", "expected": "30"}
        ]
    },
    {
        "id": "P006",
        "title": "Count Vowels",
        "difficulty": "easy",
        "description": "Given a string, count the number of vowels (a, e, i, o, u). Case-insensitive.",
        "constraints": "1 <= s.length <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["string"],
        "examples": [
            {"input": "hello", "output": "2"}
        ],
        "starter_code": {
            "python": "def solve(input_data):\n    # Write your solution here\n    pass",
            "javascript": "function solve(s) {\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        if(scanner.hasNextLine()) {\n            String s = scanner.nextLine();\n            // Write your solution here\n        }\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "hello", "expected": "2", "description": "Basic"},
            {"input": "APPLE", "expected": "2", "description": "Uppercase"}
        ],
        "hidden_test_cases": [
            {"input": "xyz", "expected": "0"},
            {"input": "aeiouAEIOU", "expected": "10"},
            {"input": "a", "expected": "1"}
        ]
    },
    {
        "id": "P007",
        "title": "Fibonacci",
        "difficulty": "easy",
        "description": "Compute the nth Fibonacci number. F(0) = 0, F(1) = 1.",
        "constraints": "0 <= n <= 30",
        "time_limit_seconds": 5,
        "tags": ["math"],
        "examples": [
            {"input": "2", "output": "1"}
        ],
        "starter_code": {
            "python": "def solve(input_data):\n    n = int(input_data)\n    # Write your solution here\n    pass",
            "javascript": "function solve(n) {\n    const data = parseInt(n);\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        int n = scanner.nextInt();\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "2", "expected": "1", "description": "F(2)"},
            {"input": "4", "expected": "3", "description": "F(4)"}
        ],
        "hidden_test_cases": [
            {"input": "0", "expected": "0"},
            {"input": "1", "expected": "1"},
            {"input": "10", "expected": "55"}
        ]
    },
    {
        "id": "P008",
        "title": "Valid Parentheses",
        "difficulty": "medium",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "constraints": "1 <= s.length <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["stack", "string"],
        "examples": [
            {"input": "()[]{}", "output": "true"}
        ],
        "starter_code": {
            "python": "def solve(input_data):\n    # Return True or False\n    pass",
            "javascript": "function solve(s) {\n    // Return true or false\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        if(scanner.hasNextLine()) {\n            String s = scanner.nextLine();\n            // Write your solution here\n        }\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "()", "expected": "true", "description": "Simple"},
            {"input": "(]", "expected": "false", "description": "Mismatched"}
        ],
        "hidden_test_cases": [
            {"input": "([)]", "expected": "false"},
            {"input": "{[]}", "expected": "true"},
            {"input": "]", "expected": "false"}
        ]
    },
    {
        "id": "P009",
        "title": "Binary Search",
        "difficulty": "medium",
        "description": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.",
        "constraints": "1 <= nums.length <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["binary-search", "array"],
        "examples": [
            {"input": "[-1,0,3,5,9,12]\n9", "output": "4"}
        ],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nums = ast.literal_eval(lines[0])\n    target = int(lines[1])\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split('\\n');\n    const nums = JSON.parse(lines[0]);\n    const target = parseInt(lines[1]);\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[-1,0,3,5,9,12]\n9", "expected": "4", "description": "Found"},
            {"input": "[-1,0,3,5,9,12]\n2", "expected": "-1", "description": "Not found"}
        ],
        "hidden_test_cases": [
            {"input": "[5]\n5", "expected": "0"},
            {"input": "[5]\n-5", "expected": "-1"},
            {"input": "[1,2,3,4,5]\n5", "expected": "4"}
        ]
    },
    {
        "id": "P010",
        "title": "Maximum Subarray",
        "difficulty": "medium",
        "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
        "constraints": "1 <= nums.length <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array", "dynamic-programming"],
        "examples": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"}
        ],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    nums = ast.literal_eval(input_data)\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const nums = JSON.parse(data);\n    // Write your solution here\n}",
            "java": "import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected": "6", "description": "Mixed"},
            {"input": "[1]", "expected": "1", "description": "Single"}
        ],
        "hidden_test_cases": [
            {"input": "[5,4,-1,7,8]", "expected": "23"},
            {"input": "[-1,-2,-3,-4]", "expected": "-1"},
            {"input": "[-2,1]", "expected": "1"}
        ]
    },
    {
        "id": "P011",
        "title": "Sum of Digits",
        "difficulty": "easy",
        "description": "Given a non-negative integer n, return the sum of its digits.",
        "constraints": "0 <= n <= 10^18",
        "time_limit_seconds": 5,
        "tags": ["math"],
        "examples": [{"input": "12345", "output": "15"}],
        "starter_code": {
            "python": "def solve(input_data):\n    n = input_data.strip()\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const n = data.trim();\n    // Write your solution here\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String n = sc.hasNextLine() ? sc.nextLine().trim() : \"\";\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "12345", "expected": "15", "description": "Basic"},
            {"input": "0", "expected": "0", "description": "Zero"}
        ],
        "hidden_test_cases": [
            {"input": "999999999999999999", "expected": "162"},
            {"input": "10", "expected": "1"},
            {"input": "100000", "expected": "1"}
        ]
    },
    {
        "id": "P012",
        "title": "Count Words",
        "difficulty": "easy",
        "description": "Given a line of text, return the number of words (separated by one or more spaces).",
        "constraints": "0 <= text length <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["string"],
        "examples": [{"input": "hello world", "output": "2"}],
        "starter_code": {
            "python": "def solve(input_data):\n    s = input_data\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const s = data;\n    // Write your solution here\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine() : \"\";\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "hello world", "expected": "2", "description": "Two words"},
            {"input": "   a   b  c  ", "expected": "3", "description": "Extra spaces"}
        ],
        "hidden_test_cases": [
            {"input": "", "expected": "0"},
            {"input": "one", "expected": "1"},
            {"input": "a  b   ", "expected": "2"}
        ]
    },
    {
        "id": "P013",
        "title": "Is Prime",
        "difficulty": "easy",
        "description": "Given an integer n, return true if n is prime, otherwise false.",
        "constraints": "-10^9 <= n <= 10^9",
        "time_limit_seconds": 5,
        "tags": ["math"],
        "examples": [{"input": "7", "output": "true"}],
        "starter_code": {
            "python": "def solve(input_data):\n    n = int(input_data.strip())\n    # Return True or False\n    pass",
            "javascript": "function solve(data) {\n    const n = parseInt(data.trim());\n    // Return true or false\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        long n = sc.hasNextLong() ? sc.nextLong() : 0;\n        // Print true or false\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "7", "expected": "true", "description": "Prime"},
            {"input": "1", "expected": "false", "description": "Not prime"}
        ],
        "hidden_test_cases": [
            {"input": "2", "expected": "true"},
            {"input": "0", "expected": "false"},
            {"input": "-17", "expected": "false"}
        ]
    },
    {
        "id": "P014",
        "title": "GCD of Two Numbers",
        "difficulty": "easy",
        "description": "Given two integers a and b, return their greatest common divisor.",
        "constraints": "-10^9 <= a,b <= 10^9",
        "time_limit_seconds": 5,
        "tags": ["math"],
        "examples": [{"input": "12 18", "output": "6"}],
        "starter_code": {
            "python": "def solve(input_data):\n    a, b = map(int, input_data.strip().split())\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const [a,b] = data.trim().split(/\\s+/).map(Number);\n    // Write your solution here\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        long a = sc.hasNextLong()? sc.nextLong():0;\n        long b = sc.hasNextLong()? sc.nextLong():0;\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "12 18", "expected": "6", "description": "Basic"},
            {"input": "7 13", "expected": "1", "description": "Coprime"}
        ],
        "hidden_test_cases": [
            {"input": "0 5", "expected": "5"},
            {"input": "-24 18", "expected": "6"},
            {"input": "1000000000 500000000", "expected": "500000000"}
        ]
    },
    {
        "id": "P015",
        "title": "LCM of Two Numbers",
        "difficulty": "easy",
        "description": "Given two integers a and b, return their least common multiple.",
        "constraints": "0 <= a,b <= 10^9",
        "time_limit_seconds": 5,
        "tags": ["math"],
        "examples": [{"input": "4 6", "output": "12"}],
        "starter_code": {
            "python": "def solve(input_data):\n    a, b = map(int, input_data.strip().split())\n    # Write your solution here\n    pass",
            "javascript": "function solve(data) {\n    const [a,b] = data.trim().split(/\\s+/).map(Number);\n    // Write your solution here\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    static long gcd(long a,long b){a=Math.abs(a);b=Math.abs(b);while(b!=0){long t=a%b;a=b;b=t;}return a;}\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        long a = sc.hasNextLong()? sc.nextLong():0;\n        long b = sc.hasNextLong()? sc.nextLong():0;\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "4 6", "expected": "12", "description": "Basic"},
            {"input": "0 5", "expected": "0", "description": "Zero"}
        ],
        "hidden_test_cases": [
            {"input": "21 6", "expected": "42"},
            {"input": "1 999", "expected": "999"},
            {"input": "100000 100000", "expected": "100000"}
        ]
    },
    {
        "id": "P016",
        "title": "Rotate Array Right",
        "difficulty": "easy",
        "description": "Given an array nums and integer k, rotate the array to the right by k steps and return the rotated array.",
        "constraints": "1 <= nums.length <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["array"],
        "examples": [{"input": "[1,2,3,4,5]\n2", "output": "[4,5,1,2,3]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nums = ast.literal_eval(lines[0])\n    k = int(lines[1])\n    # Return rotated list\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const nums = JSON.parse(lines[0]);\n    const k = parseInt(lines[1]);\n    // Return rotated array\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Input format: first line JSON-like array, second line k\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,2,3,4,5]\n2", "expected": "[4,5,1,2,3]", "description": "Rotate by 2"},
            {"input": "[1]\n10", "expected": "[1]", "description": "Single element"}
        ],
        "hidden_test_cases": [
            {"input": "[1,2,3]\n3", "expected": "[1,2,3]"},
            {"input": "[1,2,3]\n4", "expected": "[3,1,2]"},
            {"input": "[0,0,0]\n1", "expected": "[0,0,0]"}
        ]
    },
    {
        "id": "P017",
        "title": "Remove Duplicates from Sorted Array",
        "difficulty": "easy",
        "description": "Given a sorted array, return the number of unique elements and print the unique array as JSON on one line: count then newline then array.",
        "constraints": "0 <= nums.length <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array", "two-pointers"],
        "examples": [{"input": "[1,1,2,2,3]", "output": "3\n[1,2,3]"}],
        "starter_code": {
            "python": "import ast, json\n\ndef solve(input_data):\n    nums = ast.literal_eval(input_data)\n    # Return a tuple: (count, unique_list)\n    pass",
            "javascript": "function solve(data) {\n    const nums = JSON.parse(data);\n    // Return [count, uniqueArray]\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine().trim():\"[]\";\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,1,2,2,3]", "expected": "3\n[1,2,3]", "description": "Basic"},
            {"input": "[]", "expected": "0\n[]", "description": "Empty"}
        ],
        "hidden_test_cases": [
            {"input": "[1,1,1]", "expected": "1\n[1]"},
            {"input": "[1,2,3]", "expected": "3\n[1,2,3]"},
            {"input": "[0,0,1,1,1,2,2,3,3,4]", "expected": "5\n[0,1,2,3,4]"}
        ]
    },
    {
        "id": "P018",
        "title": "Valid Anagram",
        "difficulty": "easy",
        "description": "Given two strings s and t on separate lines, return true if t is an anagram of s.",
        "constraints": "0 <= length <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["string", "hash-table"],
        "examples": [{"input": "anagram\nnagaram", "output": "true"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = input_data.split('\\n')\n    s = lines[0].strip() if len(lines)>0 else ''\n    t = lines[1].strip() if len(lines)>1 else ''\n    # Return True/False\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split('\\n');\n    const s = (lines[0]||'').trim();\n    const t = (lines[1]||'').trim();\n    // Return true/false\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine():\"\";\n        String t = sc.hasNextLine()? sc.nextLine():\"\";\n        // Print true/false\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "anagram\nnagaram", "expected": "true", "description": "Anagram"},
            {"input": "rat\ncar", "expected": "false", "description": "Not anagram"}
        ],
        "hidden_test_cases": [
            {"input": "\n", "expected": "true"},
            {"input": "a\nab", "expected": "false"},
            {"input": "aacc\nccac", "expected": "false"}
        ]
    },
    {
        "id": "P019",
        "title": "Two Sum II (Sorted)",
        "difficulty": "medium",
        "description": "Given a sorted array and a target, return indices (0-based) of two numbers that sum to target as JSON array.",
        "constraints": "2 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array", "two-pointers"],
        "examples": [{"input": "[2,7,11,15]\n9", "output": "[0,1]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nums = ast.literal_eval(lines[0])\n    target = int(lines[1])\n    # Return [i,j]\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const nums = JSON.parse(lines[0]);\n    const target = parseInt(lines[1]);\n    // Return [i,j]\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[2,7,11,15]\n9", "expected": "[0,1]", "description": "Basic"},
            {"input": "[1,2,3,4,4,9]\n8", "expected": "[3,4]", "description": "Duplicates"}
        ],
        "hidden_test_cases": [
            {"input": "[-3,-1,0,2,4]\n1", "expected": "[1,3]"},
            {"input": "[0,0,3,4]\n0", "expected": "[0,1]"},
            {"input": "[5,25,75]\n100", "expected": "[1,2]"}
        ]
    },
    {
        "id": "P020",
        "title": "Longest Common Prefix",
        "difficulty": "easy",
        "description": "Given strings on separate lines, return the longest common prefix.",
        "constraints": "1 <= number of strings <= 200",
        "time_limit_seconds": 5,
        "tags": ["string"],
        "examples": [{"input": "flower\nflow\nflight", "output": "fl"}],
        "starter_code": {
            "python": "def solve(input_data):\n    strs = [line.rstrip('\\n') for line in input_data.splitlines()]\n    # Return prefix\n    pass",
            "javascript": "function solve(data) {\n    const strs = data.split(/\\r?\\n/).filter(x=>x!==undefined);\n    // Return prefix\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        ArrayList<String> list = new ArrayList<>();\n        while(sc.hasNextLine()) list.add(sc.nextLine());\n        // Print prefix\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "flower\nflow\nflight", "expected": "fl", "description": "Common prefix"},
            {"input": "dog\nracecar\ncar", "expected": "", "description": "No prefix"}
        ],
        "hidden_test_cases": [
            {"input": "a", "expected": "a"},
            {"input": "aa\naa", "expected": "aa"},
            {"input": "ab\nabc\nabcd", "expected": "ab"}
        ]
    },
    {
        "id": "P021",
        "title": "Climbing Stairs",
        "difficulty": "easy",
        "description": "Given n, return the number of distinct ways to climb to the top if you can climb 1 or 2 steps.",
        "constraints": "1 <= n <= 45",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming"],
        "examples": [{"input": "3", "output": "3"}],
        "starter_code": {
            "python": "def solve(input_data):\n    n = int(input_data.strip())\n    # Return ways\n    pass",
            "javascript": "function solve(data) {\n    const n = parseInt(data.trim());\n    // Return ways\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.hasNextInt()? sc.nextInt():0;\n        // Print ways\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "2", "expected": "2", "description": "n=2"},
            {"input": "3", "expected": "3", "description": "n=3"}
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "1"},
            {"input": "4", "expected": "5"},
            {"input": "10", "expected": "89"}
        ]
    },
    {
        "id": "P022",
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "easy",
        "description": "Given prices array, return the maximum profit (buy once, sell once).",
        "constraints": "1 <= prices.length <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array"],
        "examples": [{"input": "[7,1,5,3,6,4]", "output": "5"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    prices = ast.literal_eval(input_data)\n    # Return max profit\n    pass",
            "javascript": "function solve(data) {\n    const prices = JSON.parse(data);\n    // Return max profit\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[7,1,5,3,6,4]", "expected": "5", "description": "Profit"},
            {"input": "[7,6,4,3,1]", "expected": "0", "description": "No profit"}
        ],
        "hidden_test_cases": [
            {"input": "[1,2]", "expected": "1"},
            {"input": "[2,4,1]", "expected": "2"},
            {"input": "[3,3,3]", "expected": "0"}
        ]
    },
    {
        "id": "P023",
        "title": "Merge Two Sorted Lists",
        "difficulty": "easy",
        "description": "Given two sorted arrays A and B (each on its own line), merge them and return the merged sorted array as JSON.",
        "constraints": "0 <= len(A)+len(B) <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array", "two-pointers"],
        "examples": [{"input": "[1,2,4]\n[1,3,4]", "output": "[1,1,2,3,4,4]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    a = ast.literal_eval(lines[0]) if lines[0].strip() else []\n    b = ast.literal_eval(lines[1]) if len(lines)>1 and lines[1].strip() else []\n    # Return merged list\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const a = JSON.parse(lines[0] || '[]');\n    const b = JSON.parse(lines[1] || '[]');\n    // Return merged array\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,2,4]\n[1,3,4]", "expected": "[1,1,2,3,4,4]", "description": "Basic"},
            {"input": "[]\n[0]", "expected": "[0]", "description": "One empty"}
        ],
        "hidden_test_cases": [
            {"input": "[]\n[]", "expected": "[]"},
            {"input": "[1]\n[]", "expected": "[1]"},
            {"input": "[-3,-1,2]\n[-2,0,3]", "expected": "[-3,-2,-1,0,2,3]"}
        ]
    },
    {
        "id": "P024",
        "title": "Minimum in Rotated Sorted Array",
        "difficulty": "medium",
        "description": "Given a rotated sorted array with unique elements, return the minimum element.",
        "constraints": "1 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["binary-search", "array"],
        "examples": [{"input": "[3,4,5,1,2]", "output": "1"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    nums = ast.literal_eval(input_data)\n    # Return min\n    pass",
            "javascript": "function solve(data) {\n    const nums = JSON.parse(data);\n    // Return min\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[3,4,5,1,2]", "expected": "1", "description": "Rotated"},
            {"input": "[11,13,15,17]", "expected": "11", "description": "Not rotated"}
        ],
        "hidden_test_cases": [
            {"input": "[2,1]", "expected": "1"},
            {"input": "[5,6,7,0,1,2,3,4]", "expected": "0"},
            {"input": "[1]", "expected": "1"}
        ]
    },
    {
        "id": "P025",
        "title": "Kth Largest Element",
        "difficulty": "medium",
        "description": "Given an array nums and integer k on next line, return the kth largest element.",
        "constraints": "1 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["heap", "array"],
        "examples": [{"input": "[3,2,1,5,6,4]\n2", "output": "5"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nums = ast.literal_eval(lines[0])\n    k = int(lines[1])\n    # Return kth largest\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const nums = JSON.parse(lines[0]);\n    const k = parseInt(lines[1]);\n    // Return kth largest\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[3,2,1,5,6,4]\n2", "expected": "5", "description": "k=2"},
            {"input": "[3,2,3,1,2,4,5,5,6]\n4", "expected": "4", "description": "Duplicates"}
        ],
        "hidden_test_cases": [
            {"input": "[1]\n1", "expected": "1"},
            {"input": "[-1,-2,-3]\n1", "expected": "-1"},
            {"input": "[7,6,5,4,3,2,1]\n7", "expected": "1"}
        ]
    },
    {
        "id": "P026",
        "title": "Evaluate Reverse Polish Notation",
        "difficulty": "medium",
        "description": "Given tokens as space-separated RPN expression, evaluate and return integer result.",
        "constraints": "1 <= tokens <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["stack"],
        "examples": [{"input": "2 1 + 3 *", "output": "9"}],
        "starter_code": {
            "python": "def solve(input_data):\n    tokens = input_data.strip().split()\n    # Return int\n    pass",
            "javascript": "function solve(data) {\n    const tokens = data.trim().split(/\\s+/);\n    // Return int\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String line = sc.hasNextLine()? sc.nextLine():\"\";\n        // Print int result\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "2 1 + 3 *", "expected": "9", "description": "Basic"},
            {"input": "4 13 5 / +", "expected": "6", "description": "Division"}
        ],
        "hidden_test_cases": [
            {"input": "10 6 9 3 + -11 * / * 17 + 5 +", "expected": "22"},
            {"input": "3 4 +", "expected": "7"},
            {"input": "5 1 2 + 4 * + 3 -", "expected": "14"}
        ]
    },
    {
        "id": "P027",
        "title": "Group Anagrams",
        "difficulty": "medium",
        "description": "Given words (one per line), group anagrams and output groups as JSON array of arrays (order doesn't matter but groups should be sorted internally).",
        "constraints": "1 <= words <= 10^3",
        "time_limit_seconds": 5,
        "tags": ["hash-table", "string"],
        "examples": [{"input": "eat\ntea\ntan\nate\nnat\nbat", "output": "[[\"ate\",\"eat\",\"tea\"],[\"nat\",\"tan\"],[\"bat\"]]"}],
        "starter_code": {
            "python": "import json\n\ndef solve(input_data):\n    words = [w.strip() for w in input_data.splitlines() if w.strip()!='']\n    # Return list of groups (each group list)\n    pass",
            "javascript": "function solve(data) {\n    const words = data.split(/\\r?\\n/).map(x=>x.trim()).filter(x=>x.length);\n    // Return array of groups\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        ArrayList<String> words = new ArrayList<>();\n        while(sc.hasNextLine()){\n            String w = sc.nextLine().trim();\n            if(!w.isEmpty()) words.add(w);\n        }\n        // Print JSON-like groups\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "eat\ntea\ntan\nate\nnat\nbat", "expected": "[[\"ate\",\"eat\",\"tea\"],[\"nat\",\"tan\"],[\"bat\"]]", "description": "Example"},
            {"input": "abc\nbca\ncab\nxyz", "expected": "[[\"abc\",\"bca\",\"cab\"],[\"xyz\"]]", "description": "Two groups"}
        ],
        "hidden_test_cases": [
            {"input": "a", "expected": "[[\"a\"]]"},
            {"input": "ab\nba\nab", "expected": "[[\"ab\",\"ab\",\"ba\"]]"},
            {"input": "listen\nsilent\nenlist\ninlets", "expected": "[[\"enlist\",\"inlets\",\"listen\",\"silent\"]]"}
        ]
    },
    {
        "id": "P028",
        "title": "Coin Change (Minimum Coins)",
        "difficulty": "hard",
        "description": "Given coin denominations as JSON array and amount on next line, return minimum coins to make amount or -1.",
        "constraints": "1 <= coins <= 100, 0 <= amount <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming"],
        "examples": [{"input": "[1,2,5]\n11", "output": "3"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    coins = ast.literal_eval(lines[0])\n    amount = int(lines[1])\n    # Return min coins or -1\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const coins = JSON.parse(lines[0]);\n    const amount = parseInt(lines[1]);\n    // Return min coins or -1\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,2,5]\n11", "expected": "3", "description": "Basic"},
            {"input": "[2]\n3", "expected": "-1", "description": "Impossible"}
        ],
        "hidden_test_cases": [
            {"input": "[1]\n0", "expected": "0"},
            {"input": "[1,3,4]\n6", "expected": "2"},
            {"input": "[2,5,10,1]\n27", "expected": "4"}
        ]
    },
    {
        "id": "P029",
        "title": "Longest Increasing Subsequence",
        "difficulty": "hard",
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "constraints": "1 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["binary-search", "dynamic-programming"],
        "examples": [{"input": "[10,9,2,5,3,7,101,18]", "output": "4"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    nums = ast.literal_eval(input_data)\n    # Return LIS length\n    pass",
            "javascript": "function solve(data) {\n    const nums = JSON.parse(data);\n    // Return LIS length\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[10,9,2,5,3,7,101,18]", "expected": "4", "description": "Classic"},
            {"input": "[0,1,0,3,2,3]", "expected": "4", "description": "Mixed"}
        ],
        "hidden_test_cases": [
            {"input": "[7,7,7,7,7]", "expected": "1"},
            {"input": "[1,2,3,4,5]", "expected": "5"},
            {"input": "[5,4,3,2,1]", "expected": "1"}
        ]
    },
    {
        "id": "P030",
        "title": "Edit Distance",
        "difficulty": "hard",
        "description": "Given two strings s and t (two lines), return the minimum number of operations (insert/delete/replace) to convert s to t.",
        "constraints": "0 <= length <= 2000",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming", "string"],
        "examples": [{"input": "horse\nros", "output": "3"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = input_data.split('\\n')\n    s = lines[0].rstrip('\\n') if len(lines)>0 else ''\n    t = lines[1].rstrip('\\n') if len(lines)>1 else ''\n    # Return distance\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split(/\\r?\\n/);\n    const s = (lines[0]||'');\n    const t = (lines[1]||'');\n    // Return distance\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine():\"\";\n        String t = sc.hasNextLine()? sc.nextLine():\"\";\n        // Print distance\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "horse\nros", "expected": "3", "description": "Example"},
            {"input": "intention\nexecution", "expected": "5", "description": "Classic"}
        ],
        "hidden_test_cases": [
            {"input": "\n", "expected": "0"},
            {"input": "a\n", "expected": "1"},
            {"input": "\na", "expected": "1"}
        ]
    },
    {
        "id": "P031",
        "title": "Number of Islands",
        "difficulty": "medium",
        "description": "Given a grid of 0/1 lines of equal length, count the number of islands (4-directional). Input: first line r c, then r lines.",
        "constraints": "1 <= r,c <= 200",
        "time_limit_seconds": 5,
        "tags": ["graph", "dfs", "bfs"],
        "examples": [{"input": "3 4\n1100\n1100\n0011", "output": "2"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = input_data.strip().split('\\n')\n    r, c = map(int, lines[0].split())\n    grid = [list(lines[i+1].strip()) for i in range(r)]\n    # Return island count\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split(/\\r?\\n/);\n    const [r,c] = lines[0].trim().split(/\\s+/).map(Number);\n    const grid = [];\n    for(let i=0;i<r;i++) grid.push(lines[i+1].trim().split(''));\n    // Return island count\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int r = sc.nextInt();\n        int c = sc.nextInt();\n        sc.nextLine();\n        char[][] grid = new char[r][c];\n        for(int i=0;i<r;i++){\n            String line = sc.nextLine().trim();\n            for(int j=0;j<c;j++) grid[i][j] = line.charAt(j);\n        }\n        // Print island count\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "3 4\n1100\n1100\n0011", "expected": "2", "description": "Two blocks"},
            {"input": "2 2\n00\n00", "expected": "0", "description": "No land"}
        ],
        "hidden_test_cases": [
            {"input": "1 1\n1", "expected": "1"},
            {"input": "1 5\n10101", "expected": "3"},
            {"input": "3 3\n111\n010\n111", "expected": "1"}
        ]
    },
    {
        "id": "P032",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "description": "Given nums as JSON array and integer k on next line, return the k most frequent elements as JSON array (any order).",
        "constraints": "1 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["hash-table", "heap"],
        "examples": [{"input": "[1,1,1,2,2,3]\n2", "output": "[1,2]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nums = ast.literal_eval(lines[0])\n    k = int(lines[1])\n    # Return list of k elements\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const nums = JSON.parse(lines[0]);\n    const k = parseInt(lines[1]);\n    // Return array\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,1,1,2,2,3]\n2", "expected": "[1,2]", "description": "Example"},
            {"input": "[4,4,4,6,6,7]\n1", "expected": "[4]", "description": "Top 1"}
        ],
        "hidden_test_cases": [
            {"input": "[1]\n1", "expected": "[1]"},
            {"input": "[1,2]\n2", "expected": "[1,2]"},
            {"input": "[2,2,3,3,3]\n1", "expected": "[3]"}
        ]
    },
    {
        "id": "P033",
        "title": "Detect Cycle in Linked List",
        "difficulty": "hard",
        "description": "Given an array of next indices and a head index, detect if there's a cycle. Input: next as JSON array, then head. -1 means null. Return true/false.",
        "constraints": "0 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["two-pointers"],
        "examples": [{"input": "[1,2,3,1]\n0", "output": "true"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    nxt = ast.literal_eval(lines[0])\n    head = int(lines[1])\n    # Return True/False\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const nxt = JSON.parse(lines[0]);\n    const head = parseInt(lines[1]);\n    // Return true/false\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,2,3,1]\n0", "expected": "true", "description": "Cycle exists"},
            {"input": "[1,2,-1]\n0", "expected": "false", "description": "No cycle"}
        ],
        "hidden_test_cases": [
            {"input": "[]\n0", "expected": "false"},
            {"input": "[0]\n0", "expected": "true"},
            {"input": "[2,0,1]\n0", "expected": "true"}
        ]
    },
    {
        "id": "P034",
        "title": "Median of Two Sorted Arrays",
        "difficulty": "hard",
        "description": "Given two sorted arrays A and B (two lines), return their median as a number (integer or .5).",
        "constraints": "0 <= m+n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["binary-search", "array"],
        "examples": [{"input": "[1,3]\n[2]", "output": "2"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    a = ast.literal_eval(lines[0]) if lines[0].strip() else []\n    b = ast.literal_eval(lines[1]) if len(lines)>1 and lines[1].strip() else []\n    # Return median number\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split('\\n');\n    const a = JSON.parse(lines[0] || '[]');\n    const b = JSON.parse(lines[1] || '[]');\n    // Return median\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[1,3]\n[2]", "expected": "2", "description": "Odd total"},
            {"input": "[1,2]\n[3,4]", "expected": "2.5", "description": "Even total"}
        ],
        "hidden_test_cases": [
            {"input": "[]\n[1]", "expected": "1"},
            {"input": "[0,0]\n[0,0]", "expected": "0"},
            {"input": "[2]\n[]", "expected": "2"}
        ]
    },
    {
        "id": "P035",
        "title": "Trapping Rain Water",
        "difficulty": "hard",
        "description": "Given heights array, compute how much water it can trap.",
        "constraints": "0 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["two-pointers", "stack"],
        "examples": [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    h = ast.literal_eval(input_data)\n    # Return trapped water\n    pass",
            "javascript": "function solve(data) {\n    const h = JSON.parse(data);\n    // Return trapped water\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected": "6", "description": "Classic"},
            {"input": "[4,2,0,3,2,5]", "expected": "9", "description": "Another"}
        ],
        "hidden_test_cases": [
            {"input": "[]", "expected": "0"},
            {"input": "[1,2,3]", "expected": "0"},
            {"input": "[3,2,1,2,3]", "expected": "4"}
        ]
    },
    {
        "id": "P036",
        "title": "Longest Palindromic Substring",
        "difficulty": "medium",
        "description": "Given a string s, return the longest palindromic substring.",
        "constraints": "1 <= length <= 2000",
        "time_limit_seconds": 5,
        "tags": ["string", "dynamic-programming"],
        "examples": [{"input": "babad", "output": "bab"}],
        "starter_code": {
            "python": "def solve(input_data):\n    s = input_data.strip('\\n')\n    # Return longest palindrome substring\n    pass",
            "javascript": "function solve(data) {\n    const s = data.replace(/\\r?\\n/g,'');\n    // Return longest palindrome\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine():\"\";\n        // Print palindrome\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "babad", "expected": "bab", "description": "One valid"},
            {"input": "cbbd", "expected": "bb", "description": "Even"}
        ],
        "hidden_test_cases": [
            {"input": "a", "expected": "a"},
            {"input": "aaaa", "expected": "aaaa"},
            {"input": "abacdfgdcaba", "expected": "aba"}
        ]
    },
    {
        "id": "P037",
        "title": "Minimum Window Substring",
        "difficulty": "hard",
        "description": "Given strings s and t (two lines), return the minimum window substring of s that contains all characters of t. Return empty string if impossible.",
        "constraints": "1 <= |s|,|t| <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["string", "sliding-window"],
        "examples": [{"input": "ADOBECODEBANC\nABC", "output": "BANC"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = input_data.split('\\n')\n    s = lines[0].rstrip('\\n') if len(lines)>0 else ''\n    t = lines[1].rstrip('\\n') if len(lines)>1 else ''\n    # Return min window\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split(/\\r?\\n/);\n    const s = (lines[0]||'');\n    const t = (lines[1]||'');\n    // Return min window\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine():\"\";\n        String t = sc.hasNextLine()? sc.nextLine():\"\";\n        // Print min window\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "ADOBECODEBANC\nABC", "expected": "BANC", "description": "Example"},
            {"input": "a\na", "expected": "a", "description": "Same"}
        ],
        "hidden_test_cases": [
            {"input": "a\nb", "expected": ""},
            {"input": "aa\naa", "expected": "aa"},
            {"input": "ab\nb", "expected": "b"}
        ]
    },
    {
        "id": "P038",
        "title": "Dijkstra Shortest Path",
        "difficulty": "hard",
        "description": "Compute shortest path from source in weighted graph. Input: n m, then m lines (u v w), then source. Nodes 0..n-1. Output distances as JSON array (use -1 for unreachable).",
        "constraints": "1 <= n <= 10^5, 0 <= m <= 2*10^5",
        "time_limit_seconds": 5,
        "tags": ["graph", "dijkstra", "heap"],
        "examples": [{"input": "5 6\n0 1 2\n0 2 5\n1 2 1\n1 3 2\n2 3 1\n3 4 3\n0", "output": "[0,2,3,4,7]"}],
        "starter_code": {
            "python": "import json\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    n, m = map(int, lines[0].split())\n    edges = [tuple(map(int, lines[i+1].split())) for i in range(m)]\n    src = int(lines[m+1])\n    # Return list distances\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split(/\\r?\\n/);\n    const [n,m] = lines[0].trim().split(/\\s+/).map(Number);\n    const edges = [];\n    for(let i=0;i<m;i++) edges.push(lines[i+1].trim().split(/\\s+/).map(Number));\n    const src = parseInt(lines[m+1]);\n    // Return distances array\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        int m = sc.nextInt();\n        int[][] edges = new int[m][3];\n        for(int i=0;i<m;i++){edges[i][0]=sc.nextInt();edges[i][1]=sc.nextInt();edges[i][2]=sc.nextInt();}\n        int src = sc.nextInt();\n        // Print JSON array distances\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "5 6\n0 1 2\n0 2 5\n1 2 1\n1 3 2\n2 3 1\n3 4 3\n0", "expected": "[0,2,3,4,7]", "description": "Example"},
            {"input": "3 1\n0 1 5\n0", "expected": "[0,5,-1]", "description": "Unreachable"}
        ],
        "hidden_test_cases": [
            {"input": "1 0\n0", "expected": "[0]"},
            {"input": "2 1\n1 0 7\n1", "expected": "[7,0]"},
            {"input": "4 2\n0 1 1\n2 3 1\n0", "expected": "[0,1,-1,-1]"}
        ]
    },
    {
        "id": "P039",
        "title": "Minimum Path Sum",
        "difficulty": "medium",
        "description": "Given a grid of integers: first line r c, then r lines with c integers. Return minimum path sum from top-left to bottom-right moving only right/down.",
        "constraints": "1 <= r,c <= 200",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming"],
        "examples": [{"input": "3 3\n1 3 1\n1 5 1\n4 2 1", "output": "7"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = input_data.strip().split('\\n')\n    r,c = map(int, lines[0].split())\n    grid = [list(map(int, lines[i+1].split())) for i in range(r)]\n    # Return min sum\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split(/\\r?\\n/);\n    const [r,c] = lines[0].trim().split(/\\s+/).map(Number);\n    const grid = [];\n    for(let i=0;i<r;i++) grid.push(lines[i+1].trim().split(/\\s+/).map(Number));\n    // Return min sum\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int r = sc.nextInt();\n        int c = sc.nextInt();\n        int[][] g = new int[r][c];\n        for(int i=0;i<r;i++) for(int j=0;j<c;j++) g[i][j]=sc.nextInt();\n        // Print min sum\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "3 3\n1 3 1\n1 5 1\n4 2 1", "expected": "7", "description": "Example"},
            {"input": "1 1\n5", "expected": "5", "description": "Single cell"}
        ],
        "hidden_test_cases": [
            {"input": "2 2\n1 2\n1 1", "expected": "3"},
            {"input": "2 3\n1 2 3\n4 5 6", "expected": "12"},
            {"input": "3 2\n1 100\n1 100\n1 1", "expected": "4"}
        ]
    },
    {
        "id": "P040",
        "title": "Find All Duplicates",
        "difficulty": "medium",
        "description": "Given an array nums, return all elements that appear twice (as JSON array).",
        "constraints": "1 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array"],
        "examples": [{"input": "[4,3,2,7,8,2,3,1]", "output": "[2,3]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    nums = ast.literal_eval(input_data)\n    # Return list of duplicates\n    pass",
            "javascript": "function solve(data) {\n    const nums = JSON.parse(data);\n    // Return duplicates array\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[4,3,2,7,8,2,3,1]", "expected": "[2,3]", "description": "Example"},
            {"input": "[1,1,2]", "expected": "[1]", "description": "Single duplicate"}
        ],
        "hidden_test_cases": [
            {"input": "[1,2,3]", "expected": "[]"},
            {"input": "[2,2,2,2]", "expected": "[2]"},
            {"input": "[]", "expected": "[]"}
        ]
    },
    {
        "id": "P041",
        "title": "Serialize and Deserialize BST",
        "difficulty": "hard",
        "description": "Given preorder traversal of a BST as JSON array, reconstruct and output inorder traversal as JSON array.",
        "constraints": "0 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["tree", "bst"],
        "examples": [{"input": "[8,5,1,7,10,12]", "output": "[1,5,7,8,10,12]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    pre = ast.literal_eval(input_data)\n    # Return inorder list\n    pass",
            "javascript": "function solve(data) {\n    const pre = JSON.parse(data);\n    // Return inorder array\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[8,5,1,7,10,12]", "expected": "[1,5,7,8,10,12]", "description": "Example"},
            {"input": "[]", "expected": "[]", "description": "Empty"}
        ],
        "hidden_test_cases": [
            {"input": "[1]", "expected": "[1]"},
            {"input": "[2,1,3]", "expected": "[1,2,3]"},
            {"input": "[5,3,2,4,7,6,8]", "expected": "[2,3,4,5,6,7,8]"}
        ]
    },
    {
        "id": "P042",
        "title": "Regex Matching (., *)",
        "difficulty": "hard",
        "description": "Given s and p (two lines), implement regex matching with '.' and '*'. Return true/false.",
        "constraints": "0 <= |s|,|p| <= 2000",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming", "string"],
        "examples": [{"input": "aa\na*", "output": "true"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = input_data.split('\\n')\n    s = lines[0].rstrip('\\n') if len(lines)>0 else ''\n    p = lines[1].rstrip('\\n') if len(lines)>1 else ''\n    # Return True/False\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split(/\\r?\\n/);\n    const s = (lines[0]||'');\n    const p = (lines[1]||'');\n    // Return true/false\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine():\"\";\n        String p = sc.hasNextLine()? sc.nextLine():\"\";\n        // Print true/false\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "aa\na*", "expected": "true", "description": "Star"},
            {"input": "ab\n.*", "expected": "true", "description": "Dot-star"}
        ],
        "hidden_test_cases": [
            {"input": "aab\nc*a*b", "expected": "true"},
            {"input": "mississippi\nmis*is*p*.", "expected": "false"},
            {"input": "\n", "expected": "true"}
        ]
    },
    {
        "id": "P043",
        "title": "Merge Intervals",
        "difficulty": "medium",
        "description": "Given intervals as JSON array of [start,end], merge overlapping and return merged intervals as JSON.",
        "constraints": "0 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["array", "sorting"],
        "examples": [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    intervals = ast.literal_eval(input_data)\n    # Return merged intervals\n    pass",
            "javascript": "function solve(data) {\n    const intervals = JSON.parse(data);\n    // Return merged intervals\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[[1,3],[2,6],[8,10],[15,18]]", "expected": "[[1,6],[8,10],[15,18]]", "description": "Example"},
            {"input": "[[1,4],[4,5]]", "expected": "[[1,5]]", "description": "Touching"}
        ],
        "hidden_test_cases": [
            {"input": "[]", "expected": "[]"},
            {"input": "[[1,4]]", "expected": "[[1,4]]"},
            {"input": "[[1,10],[2,3],[4,5]]", "expected": "[[1,10]]"}
        ]
    },
    {
        "id": "P044",
        "title": "Meeting Rooms (Min Rooms)",
        "difficulty": "medium",
        "description": "Given meeting intervals as JSON array, return minimum number of rooms required.",
        "constraints": "0 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["heap", "sorting"],
        "examples": [{"input": "[[0,30],[5,10],[15,20]]", "output": "2"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    intervals = ast.literal_eval(input_data)\n    # Return min rooms\n    pass",
            "javascript": "function solve(data) {\n    const intervals = JSON.parse(data);\n    // Return min rooms\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "[[0,30],[5,10],[15,20]]", "expected": "2", "description": "Overlap"},
            {"input": "[[7,10],[2,4]]", "expected": "1", "description": "No overlap"}
        ],
        "hidden_test_cases": [
            {"input": "[]", "expected": "0"},
            {"input": "[[1,2],[2,3],[3,4]]", "expected": "1"},
            {"input": "[[1,10],[2,7],[3,4],[5,6]]", "expected": "3"}
        ]
    },
    {
        "id": "P045",
        "title": "LRU Cache Simulation",
        "difficulty": "hard",
        "description": "Simulate an LRU cache. Input: capacity, then one command per line: GET key or PUT key value. Output results of GETs each on new line.",
        "constraints": "1 <= ops <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["design", "hash-table"],
        "examples": [{"input": "2\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2\nPUT 4 4\nGET 1\nGET 3\nGET 4", "output": "1\n-1\n-1\n3\n4"}],
        "starter_code": {
            "python": "def solve(input_data):\n    lines = [l.strip() for l in input_data.splitlines() if l.strip()!='']\n    cap = int(lines[0])\n    ops = lines[1:]\n    # Return list of GET outputs (strings)\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.split(/\\r?\\n/).map(x=>x.trim()).filter(x=>x.length);\n    const cap = parseInt(lines[0]);\n    const ops = lines.slice(1);\n    // Return outputs joined by \\n\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int cap = sc.nextInt();\n        sc.nextLine();\n        ArrayList<String> ops = new ArrayList<>();\n        while(sc.hasNextLine()){\n            String line = sc.nextLine().trim();\n            if(!line.isEmpty()) ops.add(line);\n        }\n        // Print GET outputs\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "2\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2\nPUT 4 4\nGET 1\nGET 3\nGET 4", "expected": "1\n-1\n-1\n3\n4", "description": "Classic"},
            {"input": "1\nPUT 1 1\nGET 1\nPUT 2 2\nGET 1\nGET 2", "expected": "1\n-1\n2", "description": "Cap 1"}
        ],
        "hidden_test_cases": [
            {"input": "2\nGET 1", "expected": "-1"},
            {"input": "2\nPUT 1 1\nPUT 1 2\nGET 1", "expected": "2"},
            {"input": "3\nPUT 1 1\nPUT 2 2\nPUT 3 3\nPUT 4 4\nGET 1\nGET 2\nGET 3\nGET 4", "expected": "-1\n2\n3\n4"}
        ]
    },
    {
        "id": "P046",
        "title": "Decode Ways",
        "difficulty": "medium",
        "description": "Given a digit string s, return the number of ways to decode it (A=1..Z=26).",
        "constraints": "1 <= |s| <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming", "string"],
        "examples": [{"input": "226", "output": "3"}],
        "starter_code": {
            "python": "def solve(input_data):\n    s = input_data.strip()\n    # Return decode count\n    pass",
            "javascript": "function solve(data) {\n    const s = data.trim();\n    // Return decode count\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine().trim():\"\";\n        // Print decode count\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "226", "expected": "3", "description": "Example"},
            {"input": "06", "expected": "0", "description": "Leading zero"}
        ],
        "hidden_test_cases": [
            {"input": "10", "expected": "1"},
            {"input": "27", "expected": "1"},
            {"input": "11106", "expected": "2"}
        ]
    },
    {
        "id": "P047",
        "title": "Word Break",
        "difficulty": "hard",
        "description": "Given string s (line 1) and dictionary words as JSON array (line 2), return true if s can be segmented.",
        "constraints": "1 <= |s| <= 10^5, words <= 10^4",
        "time_limit_seconds": 5,
        "tags": ["dynamic-programming", "string"],
        "examples": [{"input": "leetcode\n[\"leet\",\"code\"]", "output": "true"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    s = lines[0].strip() if lines else ''\n    words = ast.literal_eval(lines[1]) if len(lines)>1 else []\n    # Return True/False\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split(/\\r?\\n/);\n    const s = (lines[0]||'').trim();\n    const words = JSON.parse(lines[1]||'[]');\n    // Return true/false\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine()? sc.nextLine().trim():\"\";\n        String w = sc.hasNextLine()? sc.nextLine().trim():\"[]\";\n        // Print true/false\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "leetcode\n[\"leet\",\"code\"]", "expected": "true", "description": "Example"},
            {"input": "catsandog\n[\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "expected": "false", "description": "False case"}
        ],
        "hidden_test_cases": [
            {"input": "applepenapple\n[\"apple\",\"pen\"]", "expected": "true"},
            {"input": "a\n[\"a\"]", "expected": "true"},
            {"input": "aaaaaaa\n[\"aaaa\",\"aaa\"]", "expected": "true"}
        ]
    },
    {
        "id": "P048",
        "title": "Course Schedule",
        "difficulty": "medium",
        "description": "Given numCourses n and prerequisites as JSON array of [a,b] meaning a depends on b, return true if you can finish all courses.",
        "constraints": "1 <= n <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["graph", "topological-sort"],
        "examples": [{"input": "2\n[[1,0]]", "output": "true"}],
        "starter_code": {
            "python": "import ast\n\ndef solve(input_data):\n    lines = input_data.strip().split('\\n')\n    n = int(lines[0])\n    prereq = ast.literal_eval(lines[1]) if len(lines)>1 else []\n    # Return True/False\n    pass",
            "javascript": "function solve(data) {\n    const lines = data.trim().split(/\\r?\\n/);\n    const n = parseInt(lines[0]);\n    const prereq = JSON.parse(lines[1]||'[]');\n    // Return true/false\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        sc.nextLine();\n        String p = sc.hasNextLine()? sc.nextLine().trim():\"[]\";\n        // Print true/false\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "2\n[[1,0]]", "expected": "true", "description": "Simple"},
            {"input": "2\n[[1,0],[0,1]]", "expected": "false", "description": "Cycle"}
        ],
        "hidden_test_cases": [
            {"input": "1\n[]", "expected": "true"},
            {"input": "3\n[[1,0],[2,1]]", "expected": "true"},
            {"input": "3\n[[1,0],[2,1],[0,2]]", "expected": "false"}
        ]
    },
    {
        "id": "P049",
        "title": "Minimum Stack",
        "difficulty": "easy",
        "description": "Design a stack that supports push, pop, top, and getMin in O(1). Input: one command per line. Output results of top/getMin each on new line.",
        "constraints": "1 <= ops <= 10^5",
        "time_limit_seconds": 5,
        "tags": ["stack", "design"],
        "examples": [{"input": "push 5\npush 2\ngetMin\ntop\npop\ngetMin", "output": "2\n2\n5"}],
        "starter_code": {
            "python": "def solve(input_data):\n    ops = [l.strip() for l in input_data.splitlines() if l.strip()!='']\n    # Return outputs list\n    pass",
            "javascript": "function solve(data) {\n    const ops = data.split(/\\r?\\n/).map(x=>x.trim()).filter(x=>x.length);\n    // Return outputs joined by \\n\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        ArrayList<String> ops = new ArrayList<>();\n        while(sc.hasNextLine()){\n            String line = sc.nextLine().trim();\n            if(!line.isEmpty()) ops.add(line);\n        }\n        // Print outputs\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "push 5\npush 2\ngetMin\ntop\npop\ngetMin", "expected": "2\n2\n5", "description": "Basic"},
            {"input": "push -1\ngetMin\npush -2\ngetMin\npop\ngetMin", "expected": "-1\n-2\n-1", "description": "Negatives"}
        ],
        "hidden_test_cases": [
            {"input": "push 1\ntop", "expected": "1"},
            {"input": "push 2\npush 2\ngetMin\npop\ngetMin", "expected": "2\n2"},
            {"input": "push 3\npop\ngetMin", "expected": "error"}
        ]
    },
    {
        "id": "P050",
        "title": "Integer to Roman",
        "difficulty": "medium",
        "description": "Given an integer n, convert it to Roman numeral.",
        "constraints": "1 <= n <= 3999",
        "time_limit_seconds": 5,
        "tags": ["string"],
        "examples": [{"input": "58", "output": "LVIII"}],
        "starter_code": {
            "python": "def solve(input_data):\n    n = int(input_data.strip())\n    # Return roman string\n    pass",
            "javascript": "function solve(data) {\n    const n = parseInt(data.trim());\n    // Return roman string\n}",
            "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.hasNextInt()? sc.nextInt():0;\n        // Print roman string\n    }\n}"
        },
        "visible_test_cases": [
            {"input": "58", "expected": "LVIII", "description": "58"},
            {"input": "1994", "expected": "MCMXCIV", "description": "1994"}
        ],
        "hidden_test_cases": [
            {"input": "3", "expected": "III"},
            {"input": "9", "expected": "IX"},
            {"input": "3999", "expected": "MMMCMXCIX"}
        ]
    }
]

async def seed_problems(db):
    from sqlalchemy import select
    from app.models.problem import Problem
    
    result = await db.execute(select(Problem))
    existing = result.scalars().all()
    
    # We always update the existing problems to the new starter code in this run
    for data in PROBLEMS_DATA:
        result = await db.execute(select(Problem).where(Problem.id == data["id"]))
        p = result.scalar_one_or_none()
        if p:
            # Update starter code and description
            p.starter_code = data["starter_code"]
            p.description = data["description"]
            p.title = data["title"]
            p.difficulty = data["difficulty"]
            # To be safe, update test cases too if they changed
            p.visible_test_cases = data["visible_test_cases"]
            p.hidden_test_cases = data["hidden_test_cases"]
        else:
            p = Problem(**data)
            db.add(p)
            
    await db.commit()
    print(f"Updated/Seeded {len(PROBLEMS_DATA)} problems")

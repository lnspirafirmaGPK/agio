<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MOS Desktop Terminal - Inspirafirma</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --mos-bg: #050a05;
            --mos-border: #1a331a;
            --mos-text: #4ade80; /* Green-400 */
            --mos-dim: #14532d;
            --mos-highlight: #22c55e;
        }

        body {
            background-color: var(--mos-bg);
            font-family: 'Share Tech Mono', monospace;
            overflow: hidden;
            color: var(--mos-text);
        }

        /* CRT Scanline Effect */
        .scanlines {
            background: linear-gradient(
                to bottom,
                rgba(255,255,255,0),
                rgba(255,255,255,0) 50%,
                rgba(0,0,0,0.2) 50%,
                rgba(0,0,0,0.2)
            );
            background-size: 100% 4px;
            position: absolute;
            pointer-events: none;
            top: 0; right: 0; bottom: 0; left: 0;
            z-index: 50;
            opacity: 0.15;
            /* No rounded corners for desktop */
        }

        .glow-text {
            text-shadow: 0 0 7px rgba(74, 222, 128, 0.6); /* เพิ่มความสว่างเล็กน้อย */
        }

        .border-mos {
            border: 1px solid var(--mos-border);
            box-shadow: 0 0 15px rgba(20, 83, 45, 0.3) inset; /* เพิ่มมิติ */
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; } /* ขยายขนาด Scrollbar */
        ::-webkit-scrollbar-track { background: var(--mos-bg); }
        ::-webkit-scrollbar-thumb { background: var(--mos-dim); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--mos-text); }

        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }

        .loading-bar {
            height: 100%;
            background-color: var(--mos-text);
            width: 0%;
            transition: width 0.2s;
            box-shadow: 0 0 10px var(--mos-text);
        }
    </style>
</head>
<body class="h-screen w-screen flex items-center justify-center">

    <div class="relative w-full h-full bg-black shadow-2xl overflow-hidden flex flex-col border-4 border-gray-800">
        
        <div class="scanlines"></div>

        <div class="h-8 flex justify-between items-center px-6 py-2 text-sm tracking-widest z-20 bg-black/90 border-b border-green-900/30">
            <span id="clock" class="text-green-500 font-bold">MOS_SYSTEM_READY</span>
            <div class="flex gap-4 opacity-80 text-xs">
                <span>[INSPIRAFIRMA_CORE]</span>
                <span>STATUS: STABLE</span>
                <span>NETWORK: ACTIVE</span>
            </div>
        </div>

        <div class="p-3 grid grid-cols-4 gap-3 text-xs uppercase tracking-wider z-10 bg-[#020502] border-b border-mos-border">
            <div class="border-mos p-2 flex flex-col items-center justify-center bg-[#050a05]/50">
                <span class="text-green-700">CPU LOAD</span>
                <span id="cpu-stat" class="text-xl font-bold glow-text">12%</span>
            </div>
            <div class="border-mos p-2 flex flex-col items-center justify-center bg-[#050a05]/50">
                <span class="text-green-700">MEM USE</span>
                <span id="mem-stat" class="text-xl font-bold glow-text">4.2GB</span>
            </div>
            <div class="border-mos p-2 flex flex-col items-center justify-center bg-[#050a05]/50">
                <span class="text-green-700">NODE ID</span>
                <span class="text-xl font-bold glow-text">AGIO-12</span>
            </div>
             <div class="border-mos p-2 flex flex-col items-center justify-center bg-[#050a05]/50">
                <span class="text-green-700">NET IO</span>
                <span class="text-xl font-bold glow-text animate-pulse">ACTIVE</span>
            </div>
        </div>

        <div id="terminal-output" class="flex-grow p-5 font-[JetBrains Mono] text-sm overflow-y-auto z-10 relative" onclick="document.getElementById('input-field').focus()">
            <div id="boot-sequence" class="mb-4"></div>
            <div id="history"></div>

            <div class="flex items-center mt-2 opacity-0 transition-opacity duration-500" id="input-line">
                <span class="text-green-600 mr-2">chelvas@mos-core</span>
                <span class="text-gray-500 mr-2">:</span>
                <span class="text-blue-400 mr-2" id="path-display">~/workspace</span>
                <span class="text-gray-500 mr-2">$</span>
                <input type="text" id="input-field" class="bg-transparent border-none outline-none text-green-300 w-full font-[JetBrains Mono] text-sm" autocomplete="off" spellcheck="false">
            </div>
        </div>

        <div class="h-8 bg-[#050a05] border-t border-green-900/50 flex items-center justify-between px-6 z-20 text-xs">
            <span class="text-green-800">GEP PROTOCOL ACTIVE | SOULBASE: FIRESTORE (LIVE)</span>
            <div class="flex gap-2">
                <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-green-500 blink">_</span>
            </div>
        </div>

    </div>

    <script>
        // --- Config ---
        const repoUrl = "https://github.com/lnspirafirmaGPK/Genesis-Gem-That-Thormilnus.git";
        const repoName = "Genesis-Gem-That-Thormilnus";

        // --- File System Setup ---
        const fileSystem = {
            "~": {
                type: "dir",
                content: {
                    "workspace": {
                        type: "dir",
                        content: {
                            // Will be populated by clone
                        }
                    },
                    "gep_config.py": { type: "file", content: "# GEP (Genesis Enforcement Principles)\nGEP_CONFIG = {...}" },
                    "core_manifest.txt": { type: "file", content: "Protocol: The Protocol of Inter-reflecting Mirrors\nActive Agent: Chelvas" }
                }
            }
        };

        // Initial Path set to root for the demo, then enters workspace
        let currentPath = "~"; 
        let currentDirObj = fileSystem["~"];
        
        // --- DOM Elements ---
        const termOut = document.getElementById('history');
        const inputField = document.getElementById('input-field');
        const inputLine = document.getElementById('input-line');
        const bootDiv = document.getElementById('boot-sequence');
        const pathDisplay = document.getElementById('path-display');
        const cpuStat = document.getElementById('cpu-stat');
        const memStat = document.getElementById('mem-stat');

        // --- Utilities ---
        const print = (text, style = '') => {
            const div = document.createElement('div');
            div.className = `mb-1 break-words whitespace-pre-wrap ${style}`;
            div.innerHTML = text;
            termOut.appendChild(div);
            scrollToBottom();
        };

        const scrollToBottom = () => {
            const container = document.getElementById('terminal-output');
            container.scrollTop = container.scrollHeight;
        };

        // --- Simulation Logic ---
        const simulateStats = () => {
            setInterval(() => {
                cpuStat.innerText = Math.floor(Math.random() * 20 + 5) + "%";
                memStat.innerText = (Math.random() * 1.0 + 8.0).toFixed(1) + "GB"; // เพิ่ม RAM สำหรับ Desktop
            }, 1500);
            
            setInterval(() => {
                const clock = document.getElementById('clock');
                const now = new Date();
                const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
                const dateStr = now.toLocaleDateString('en-GB'); // ใช้ DD/MM/YYYY
                clock.innerText = `MOS_V3.1 | ${dateStr} | ${timeStr}`;
            }, 1000);
        };

        const delay = ms => new Promise(res => setTimeout(res, ms));

        // --- Commands ---
        const commands = {
            ls: () => {
                if (!currentDirObj.content) {
                    print(`Error: Not a directory`, "text-red-400");
                    return;
                }
                const items = Object.keys(currentDirObj.content).map(name => {
                    const isDir = currentDirObj.content[name].type === 'dir';
                    return `<span class="${isDir ? 'text-blue-400 font-bold' : 'text-green-200'}">${name}${isDir ? '/' : ''}</span>`;
                });
                if (items.length === 0) print("(empty directory)", "text-gray-600 italic");
                else print(items.join('\t')); // ใช้ tab space สำหรับ desktop
            },
            help: () => {
                print("AGIO MOS v3.1 Console Commands:", "text-green-400 font-bold");
                print("  ls      | List directory contents");
                print("  cd      | Change directory (e.g., cd workspace)");
                print("  cat     | Display file content (e.g., cat README.md)");
                print("  clear   | Clear the terminal screen");
                print("  status  | Show detailed system status");
            },
            clear: () => termOut.innerHTML = "",
            status: () => {
                print("--- AGIO Core Status ---", "text-yellow-400 font-bold");
                print("GEP Protocol: ENFORCED");
                print("SoulBase Connection: LIVE (Firestore)");
                print("Active Agent: Chelvas (Reflective Loop Active)");
                print("Memory Trace: Last 5 rituals loaded.");
            },
            cat: (args) => {
                const filename = args[0];
                const content = currentDirObj.content;
                if(content && content[filename] && content[filename].type === 'file') {
                    print(content[filename].content.replace(/\n/g, '<br>'));
                } else {
                    print(`Error: File or directory not found: ${filename}`, "text-red-400");
                }
            },
            cd: (args) => {
                const target = args[0] || "~";
                let newPath = currentPath;
                let newDirObj = currentDirObj;

                if (target === "..") {
                    const pathSegments = currentPath.split('/');
                    if (pathSegments.length > 1) {
                        pathSegments.pop();
                        newPath = pathSegments.join('/');
                        newDirObj = fileSystem["~"]; // Simple demo: assumes nested structure starts from ~
                        
                        // Reconstruct object path for deeper nesting (simplified)
                        let tempObj = fileSystem["~"];
                        pathSegments.slice(1).forEach(seg => {
                            if (tempObj.content && tempObj.content[seg]) tempObj = tempObj.content[seg];
                        });
                        newDirObj = tempObj;
                    } else {
                        // Already at root
                        return;
                    }
                } else if (target === "~") {
                    newPath = "~";
                    newDirObj = fileSystem["~"];
                } else if (currentDirObj.content && currentDirObj.content[target] && currentDirObj.content[target].type === 'dir') {
                    newPath = currentPath === "~" ? "~/" + target : currentPath + "/" + target;
                    newDirObj = currentDirObj.content[target];
                } else {
                    print(`cd: ${target}: No such directory`, "text-red-400");
                    return;
                }

                currentPath = newPath;
                currentDirObj = newDirObj;
                pathDisplay.innerText = currentPath;
            },
            git: (args) => {
                if (args[0] === 'clone' && args[1] === repoUrl) {
                    runCloneSequence(args[1]);
                } else {
                    print("Usage: git clone <url>", "text-yellow-400");
                }
            }
        };

        // --- Git Clone Sequence ---
        const runCloneSequence = async (url) => {
            if (currentDirObj.content[repoName]) {
                print(`Error: Directory '${repoName}' already exists.`, "text-red-400");
                return;
            }
            
            print(`> git clone ${url}`, "text-yellow-400");
            await delay(500);
            print(`Cloning into '${repoName}'...`, "text-gray-400");
            
            // Fake Progress Bar
            const progressDiv = document.createElement('div');
            progressDiv.className = "w-96 h-3 border border-green-800 mt-2 mb-3 bg-gray-900";
            const bar = document.createElement('div');
            bar.className = "loading-bar";
            progressDiv.appendChild(bar);
            termOut.appendChild(progressDiv);

            for (let i = 0; i <= 100; i+=10) {
                bar.style.width = i + "%";
                await delay(80);
            }

            print("remote: Enumerating objects: 142, done.", "text-gray-400");
            print("remote: Total 142 (delta 24), reused 0 (delta 0)", "text-gray-400");
            print("Unpacking objects: 100% (142/142), done.", "text-gray-400");
            print(`Successfully cloned to ${currentPath === "~" ? currentPath : currentPath + "/"}${repoName}`, "text-green-400");

            // Update Filesystem
            currentDirObj.content[repoName] = {
                type: "dir",
                content: {
                    "README.md": { type: "file", content: "# Genesis Gem That Thormilnus\n\nProject MOS Integration.\nStatus: Active\nKey: 0x4F2A..." },
                    "src": { type: "dir", content: {} },
                    "config.json": { type: "file", content: "{ \"env\": \"production\" }" }
                }
            };

            // Auto Enter Directory
            commands.cd([repoName]);
        };

        // --- Boot Sequence ---
        const runBootSequence = async () => {
            const steps = [
                "BIOS: MOS Kernel Loaded.",
                "INIT: Checking GEP Protocol Integrity...",
                "SEC: CRITICAL POLICY VALIDATION [OK]",
                "NET: Establishing Uplink to SoulBase (Firestore)...",
                "[ OK ] AGIO-12 NODE IS ONLINE."
            ];

            for (const step of steps) {
                const div = document.createElement('div');
                div.innerText = step;
                div.className = "text-green-800 text-sm";
                bootDiv.appendChild(div);
                await delay(400);
            }
            
            await delay(800);
            print("MOS DESKTOP TERMINAL READY.", "text-green-400 font-bold mb-4 text-lg");
            
            // Auto Enter Workspace
            commands.cd(["workspace"]);
            
            // Simulate Auto Git Clone
            await runCloneSequence(repoUrl);

            // Ready for user
            inputLine.classList.remove('opacity-0');
            inputField.focus();
            simulateStats();
        };

        // --- Input Handler ---
        inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const val = inputField.value.trim();
                if (!val) {
                    print(`chelvas@mos-core:${currentPath}$`, "text-gray-500");
                    return;
                }
                
                print(`chelvas@mos-core:${currentPath}$ ${val}`, "text-gray-500");
                const [cmd, ...args] = val.split(' ');
                
                if (commands[cmd]) commands[cmd](args);
                else print(`bash: ${cmd}: command not found`, "text-red-400");
                
                inputField.value = "";
                scrollToBottom();
            }
        });

        window.onload = runBootSequence;

    </script>
</body>
</html>

import os
import sys
import subprocess

def setup():
    print("[*] Setting up environment...")
    if not os.path.exists("ttak.so"):
        print("[*] Compiling ttak for your device architecture...")
        try:
            subprocess.run(["python", "setup.py", "build_ext", "--inplace"], check=True)
            # Find the generated .so file and rename it to ttak.so
            for f in os.listdir("."):
                if f.startswith("ttak.cpython") and f.endswith(".so"):
                    os.rename(f, "ttak.so")
                    break
            # Clean up source files after compilation to keep only .so
            for f in ["ttak.py", "setup.py", "ttak.c"]:
                if os.path.exists(f):
                    os.remove(f)
            print("[+] Compilation successful! ttak.so created.")
        except Exception as e:
            print(f"[-] Compilation failed: {e}")
            sys.exit(1)
    
    import ttak
    ttak.start_bypass()

if __name__ == "__main__":
    setup()

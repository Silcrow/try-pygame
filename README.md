# try-pygame

# Personal Notes

1. How Buildozer Works
Buildozer is a tool that packages Python apps (like your Pygame project) into APK files for Android.
It uses a buildozer.spec file to configure the build.
When you run buildozer -v android debug (or similar), it should create an APK file, usually in the bin/ directory of your project.
2. Checking if the APK Was Built
The APK file is typically located at bin/<project_name>-<version>-debug.apk (or similar).
You can check for this file in your project directory.
3. Installing the APK on Your Phone
Once you have the APK, you can:
Transfer it to your phone (via USB, email, cloud, etc.).
Enable "Install from Unknown Sources" on your phone.
Tap the APK file to install.

## building APK

1. Build the APK with Buildozer:
- Make sure you have a buildozer.spec file in your project directory.
Run the following command in your project directory:
```bash
buildozer -v android debug
```
- This command will attempt to build a debug APK. The process can take a while the first time.
2. Check for Errors:
- If the build fails, carefully review the output for errors or missing dependencies.
- Common issues include missing system packages, Java, or Android SDK/NDK problems.
3. Find the APK:
- After a successful build, the APK should be in the bin/ directory inside your project folder.
4. Install on Your Phone:
- Transfer the APK to your phone and install it as described previously.

### Troubleshooting
The APK build failed because Buildozer (via python-for-android) requires OpenSSL 1.1, but this version has been disabled in Homebrew and cannot be installed on your system. This is a common issue on newer macOS versions, as OpenSSL 1.1 is no longer supported or available via Homebrew.

What happened?
- Buildozer tried to install openssl@1.1 using Homebrew.
- Homebrew reported that openssl@1.1 is disabled and cannot be installed.
- As a result, the build process crashed and no APK was generated.

**How to Fix This**
There are a few possible solutions:

1. Use OpenSSL 3.x (if python-for-android supports it)
- Newer versions of python-for-android may support OpenSSL 3.x.
- You may need to update both Buildozer and python-for-android to their latest versions.
2. Manually Install OpenSSL 1.1 (not recommended, but possible)
- You could try downloading and building OpenSSL 1.1 from source, but this is complex and not recommended for most users.
3. Use a Linux VM, WSL, or Docker
- Many users build their APKs using Linux, either via a virtual machine, WSL (on Windows), or Docker.
- This avoids macOS/Homebrew issues.

Both Buildozer and python-for-android are already updated to recent versions, but the build is still failing because it requires OpenSSL 1.1, which is now disabled and unavailable via Homebrew on macOS. This is a known and currently unsolved limitation for building Android APKs with Buildozer on recent macOS versions.

Key Facts:
- Updating Buildozer and python-for-android did not resolve the OpenSSL 1.1 dependency.
- The build process cannot proceed on macOS due to the unavailability of OpenSSL 1.1.
- This is not an issue with your code or configuration, but with the build toolchain and macOS package availability.

Your Options
1. Use a Linux Environment for Building
The most reliable solution is to build your APK on a Linux machine, VM, or Docker container, where OpenSSL 1.1 is still available.
You can use a cloud VM (e.g., AWS, GCP, DigitalOcean), a local Linux PC, or set up a Linux VM on your Mac (using VirtualBox, UTM, or Parallels).
Alternatively, you can use a pre-configured Docker image for Buildozer.
2. Wait for Upstream Fixes
The Kivy/Buildozer team may eventually update their toolchain to support OpenSSL 3.x, but this is not yet the case.

I have replaced it with a minimal and robust Dockerfile using the official Kivy Buildozer image, which is purpose-built for building Android APKs and includes all necessary dependencies (including OpenSSL 1.1).
Your new Dockerfile:
```dockerfile
FROM kivy/buildozer:stable

# Set up working directory for mounting host code
WORKDIR /home/user/app
```

**Building APK with Docker**
1. Install Docker Desktop:
Download and install from https://www.docker.com/products/docker-desktop/
2. Build the Docker image:
Open a terminal in your project directory (where the Dockerfile is) and run:
```sh
docker build -t my-buildozer .
```
3. Run the Buildozer container to build your APK:
```sh
docker run --rm -it \
  -v "$PWD":/home/user/app \
  -w /home/user/app \
  my-buildozer \
  buildozer -v android debug
```
- This mounts your project into the container and runs Buildozer inside the correct directory.
4. After the build completes: Your APK will be in the bin/ directory of your project on your host machine.
5. Transfer the APK to your Android device and install it as usual.

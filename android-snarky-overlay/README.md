# Snarky Overlay Android App

This is an Android application that runs a background overlay service. It reads the text on your screen and displays snarky, judgmental remarks about what you are doing.

## Features

- **Always-on Overlay**: A floating bubble that stays on top of other apps.
- **Screen Reading**: Uses Android's `AccessibilityService` to read text content from the active window.
- **Snark Generator**: Simple logic to detect keywords (like "Instagram", "Settings", "Work") and generate context-aware snarky comments.

## Project Structure

- `app/src/main/java/com/example/snarkyoverlay/SnarkyAccessibilityService.java`: The core service. It manages the overlay window and handles accessibility events to read screen text.
- `app/src/main/java/com/example/snarkyoverlay/SnarkGenerator.java`: Logic for generating remarks.
- `app/src/main/java/com/example/snarkyoverlay/MainActivity.java`: UI for requesting necessary permissions.

## How to Build and Run

1.  **Open in Android Studio**:
    -   Open Android Studio.
    -   Select "Open an existing Android Studio project".
    -   Navigate to the `android-snarky-overlay` directory.

2.  **Build**:
    -   Wait for Gradle sync to complete.
    -   Build the project (Build > Make Project).

3.  **Run**:
    -   Connect an Android device or start an emulator.
    -   Run the app (`Run > Run 'app'`).

## Setup Permissions

Once the app is installed on your device:

1.  **Grant Overlay Permission**:
    -   Open the "Snarky Overlay" app.
    -   Click **"Grant Overlay Permission"**.
    -   Toggle the switch to allow "Display over other apps".

2.  **Enable Accessibility Service**:
    -   In the app, click **"Enable Snarky Service"**.
    -   You will be taken to Accessibility Settings.
    -   Find **"Snarky Assistant"** in the list (usually under "Downloaded Apps" or "Installed Services").
    -   Tap it and toggle it **ON**.
    -   Allow "Control" permission when prompted (this is needed to read screen content).

## Usage

After enabling the service, you will see a text bubble floating on your screen saying "I'm watching you...". Go ahead and open other apps like Instagram, Settings, or Gmail. The bubble will update with judgmental comments based on what you are doing.

## Notes

-   **Privacy**: This app reads screen content to function. It processes text locally within `SnarkGenerator`.
-   **Performance**: The service updates at most once every 3 seconds to avoid battery drain.

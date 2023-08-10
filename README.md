# SingBoxUI

SingBoxUI is a graphical user interface application that allows users to connect to the SingBox service and manage their subscription. It provides an easy-to-use interface for starting and terminating the SingBox application and accessing the SingBox dashboard.

## Features

- Connect and Disconnect: Start and stop the SingBox application with the click of a button.
- Use Local Config: Choose to use a local configuration file for customization.
- Display IP and Location: View your IP address and location information within the application.
- Save Subscription Link: Save your subscription link for easy access.
- Open SingBox Dashboard: Open the SingBox dashboard directly from the application.
- Automatic Administrator Privileges: SingBoxUI automatically requests administrator privileges for a seamless user experience.
- Latest Version Detection: Automatically detects and downloads the latest version of SingBox.
- Error Handling: Provides informative error messages in case of any issues.

## Prerequisites

- Python 3.6 or higher
- tkinter library
- urllib library

## Getting Started

1. Download Latest release from [here](https://github.com/yebekhe/SingBox-UI/releases/latest).
2. Extarct the compressed file and Run SingboxUI.exe.
1. Check [Usage](https://github.com/yebekhe/SingBox-UI/edit/main/README.md#getting-started) for more instructions .

## Usage

1. Enter your subscription link in the "SUBSCRIPTION LINK" field.
1. Check the "USE LOCAL CONFIG" checkbox if you want to use a local configuration file.
1. Click the "✅ CONNECT" button to start the SingBox application.
1. Once connected, the IP address and location will be displayed.
1. Click the "❌ DISCONNECT" button to stop the SingBox application.
1. Click the "📃 OPEN SING-BOX DASHBOARD" button to open the SingBox dashboard.

## Configuration

- Local Config File: Create a `config.ini` file in the same folder as the `SingboxUI.exe` file to use custom configurations. The file should have the following structure:

```
[Text]
Value = <subscription link>
```

## Additional Notes

- SingBoxUI requires administrator privileges to start and stop the SingBox application. Make sure to run the application as an administrator.
- SingBoxUI downloads the latest version of SingBox from the official GitHub repository.
- SingBoxUI fetches the IP address and location information using the http://ip-api.com/json/ API.

## Disclaimer

SingBoxUI is a third-party application and is not affiliated with or endorsed by the SingBox project.

## License

This project is licensed under the [AGPL-3.0 license](LICENSE).

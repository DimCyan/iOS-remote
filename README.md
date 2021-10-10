![](https://github.com/SimonWDC/ios-remote/blob/main/img/logo-1.png)

# iOS-remote

iOS-remote connects to iOS devices via USB for displaying and controlling in web browser. It does NOT require jailbreaking. Because of displaying in web browser, iOS-remote supports Linux, macOS, Windows.

![](https://github.com/SimonWDC/ios-remote/blob/main/img/mainpage.png)

## iOS Version Support

The support of this project depends on the version of WebDriverAgent. After testing, iOS15 is already supported. Please using the latest [WebDriverAgent](https://github.com/appium/WebDriverAgent).

## Download & Use

There are some necessary libraries and tools for this project:

1. [WebDriverAgent](https://github.com/appium/WebDriverAgent)

2. [Tidevice](https://github.com/alibaba/taobao-iphone-device)

3. Python libraries:

    ```pip3 install -r requirements.txt```

After installing and preparing the environment, run following command in your terminal:

1. Bild, Test and Install WebDriverAgent-Runner Into Device

    Start WebDriverAgent 👉 [Link](https://github.com/facebookarchive/WebDriverAgent/wiki/Starting-WebDriverAgent)

2. Run WebDriverAgent by using Tidevice

    ```tidevice wdaproxy -B com.facebook.wda.WebDriverAgent.Runner --port 8100```
    
    When you see `WebDriverAgent start successfully` in your terminal, you run WebDriverAgent successfully!!!!

3. Forward the request to the iOS device by using Tidevice

    ```tidevice relay 8200 9100```

    > The default port of this project is `8200`, you can change the port you like in the connect input field~

4. Run Flask Server

    ```python3 app.py```

5. Open Browser With URL `http://127.0.0.1:5000/`

## Features

1. Display

2. Switch rotation

3. Control:

    - Swipe

    - Click

4. Button operation:

    - Home button

    - Power button to lock screen

5. Screenshot

6. Send text

## TODO

1. Volume up and down buttons

2. Display more devices

3. Start up automated

4. Display app list

5. Install and Uninstall app

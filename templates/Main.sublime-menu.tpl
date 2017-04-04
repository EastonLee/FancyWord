[
    {
        "caption": "Preferences",
        "mnemonic": "f",
        "id": "preferences",
        "children":
        [
            {
                "caption": "Package Settings",
                "mnemonic": "F",
                "id": "package-settings",
                "children":
                [
                    {
                        "caption": "FancyWord",
                        "children":
                        [
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/$package_folder/README.md"},
                                "caption": "README"
                            },
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/$package_folder/LICENSE"},
                                "caption": "LICENSE"
                            },
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/$package_folder/FancyWord.sublime-settings"},
                                "caption": "Settings – Default"
                            },
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/User/FancyWord.sublime-settings"},
                                "caption": "Settings – User"
                            },
                            { "caption": "-" },
                            {
                                "command": "open_file",
                                "args": {
                                    "file": "${packages}/$package_folder/Default (OSX).sublime-keymap",
                                    "platform": "OSX"
                                },
                                "caption": "Key Bindings – Default"
                            },
                            {
                                "command": "open_file",
                                "args": {
                                    "file": "${packages}/$package_folder/Default (Linux).sublime-keymap",
                                    "platform": "Linux"
                                },
                                "caption": "Key Bindings – Default"
                            },
                            {
                                "command": "open_file",
                                "args": {
                                    "file": "${packages}/$package_folder/Default (Windows).sublime-keymap",
                                    "platform": "Windows"
                                },
                                "caption": "Key Bindings – Default"
                            },
                            {
                                "command": "open_file",
                                "args": {
                                    "file": "${packages}/User/Default (OSX).sublime-keymap",
                                    "platform": "OSX"
                                },
                                "caption": "Key Bindings – User"
                            },
                            {
                                "command": "open_file",
                                "args": {
                                    "file": "${packages}/User/Default (Linux).sublime-keymap",
                                    "platform": "Linux"
                                },
                                "caption": "Key Bindings – User"
                            },
                            {
                                "command": "open_file",
                                "args": {
                                    "file": "${packages}/User/Default (Windows).sublime-keymap",
                                    "platform": "Windows"
                                },
                                "caption": "Key Bindings – User"
                            },
                            { "caption": "-" }
                        ]
                    }
                ]
            }
        ]
    }
]
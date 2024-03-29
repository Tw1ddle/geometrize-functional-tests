// Note: you can list members of a widget with a line like "console.log(Object.getOwnPropertyNames(widget))"

function Controller() {
    // Set installer target directory to the app subfolder for testing
    installer.setValue("TargetDir", (installer.value("InstallerDirPath") + "/app"));

    // Note could auto-reject/accept message boxes here , don't expect to see any though so we won't...
    //installer.autoRejectMessageBoxes()

    installer.installationFinished.connect(function() {
        // Run the executable after installation completes
        //try {
        //    var targetDir = installer.value("TargetDir");
        //   if (installer.isInstaller() && installer.status == QInstaller.Success) {
        //        installer.executeDetached(targetDir + "/Geometrize.exe"); // TODO - run this via the self-tests, potentially a python script instead
        //    }
        //} catch(e) {
        //     print(e);
        //}

        gui.clickButton(buttons.NextButton);
    })
}

// Welcome -> Next
Controller.prototype.WelcomePageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

// Intro -> Next
Controller.prototype.IntroductionPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

// Installation Folder -> Next
Controller.prototype.TargetDirectoryPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

// Select Components -> Next
Controller.prototype.ComponentSelectionPageCallback = function() {
    var widget = gui.currentPageWidget();

    widget.selectAll();

    gui.clickButton(buttons.NextButton);
}

// Start Menu Options -> Next
Controller.prototype.StartMenuDirectoryPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

// License -> Select "I accept the license" checkbox -> Next
Controller.prototype.LicenseAgreementPageCallback = function() {
    gui.currentPageWidget().AcceptLicenseCheckBox.setChecked(true)
    gui.clickButton(buttons.NextButton);
}

// Ready To Install -> Next
Controller.prototype.ReadyForInstallationPageCallback = function() {
    gui.clickButton(buttons.CommitButton);
}

Controller.prototype.FinishedPageCallback = function() {
    var checkBoxForm = gui.currentPageWidget().LaunchAppCheckBoxForm;
    if (checkBoxForm && checkBoxForm.launchAppCheckBox) {
        checkBoxForm.launchAppCheckBox.checked = false;
    }
    gui.clickButton(buttons.FinishButton);
}
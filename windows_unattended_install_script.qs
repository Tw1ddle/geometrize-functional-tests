function Controller() {
    // Note could auto-reject/accept message boxes here , don't expect to see any though so we won't...
	//installer.autoRejectMessageBoxes()

    installer.installationFinished.connect(function() {
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
    gui.currentPageWidget().TargetDirectoryLineEdit.setText(installer.value("InstallerDirPath") + "/app");

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

// License -> Agree -> Next
Controller.prototype.LicenseAgreementPageCallback = function() {
    gui.currentPageWidget().AcceptLicenseRadioButton.setChecked(true);
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
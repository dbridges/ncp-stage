.PHONY: all ui

all:
	python3 ncp_stage_runner.py

ui:
	pyuic4 ui/NCPStageMainWindow.ui -o ui/main_window.py

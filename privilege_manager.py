# privilege_manager.py
import os
import subprocess
from enum import Enum

class SOCMode(Enum):
    USER = "USER"
    ELEVATED = "ELEVATED"
    FORENSIC = "FORENSIC"


class PrivilegeManager:
    def __init__(self):
        self.mode = self.detect_mode()

    # ---------- CORE DETECTION ----------
    def is_root(self):
        return hasattr(os, "geteuid") and os.geteuid() == 0

    def has_capabilities(self):
        """
        Checks if python has raw socket capability (Linux)
        """
        try:
            result = subprocess.run(
                ["capsh", "--print"],
                capture_output=True,
                text=True
            )
            return "cap_net_raw" in result.stdout
        except Exception:
            return False

    # ---------- MODE DECISION ENGINE ----------
    def detect_mode(self):
        if self.is_root():
            return SOCMode.ELEVATED

        if self.has_capabilities():
            return SOCMode.ELEVATED

        return SOCMode.USER

    # ---------- FORENSIC OVERRIDE ----------
    def set_forensic_mode(self):
        self.mode = SOCMode.FORENSIC

    # ---------- SAFE FEATURE GATES ----------
    def allow_network_scan(self):
        return self.mode == SOCMode.ELEVATED

    def allow_packet_capture(self):
        return self.mode == SOCMode.ELEVATED

    def allow_write_ops(self):
        return self.mode != SOCMode.FORENSIC

    # ---------- STATUS ----------
    def status(self):
        return {
            "mode": self.mode.value,
            "root": self.is_root(),
            "capabilities": self.has_capabilities()
        }
        
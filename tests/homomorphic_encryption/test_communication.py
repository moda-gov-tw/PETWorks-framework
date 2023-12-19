from unittest.mock import patch

import PETWorks.homomorphic_encryption.Communication as Communication
from scapy.all import rdpcap


@patch("scapy.all.sniff")
def testCapturePackets(mock_sniff):
    mock_sniff.return_value = ["TCP", "UDP", "TLS"]

    Communication.capturePackets(timeout=5, interface="test interface")

    mock_sniff.assert_called_with(timeout=5, iface="test interface")


def testPETValidationSuccess():
    packets = rdpcap("tests/homomorphic_encryption/tls.pcap")

    result = Communication.PETValidation(packets)

    assert result["Use TLS v1.2 or later"] is True


def testPETValidationFail():
    packets = rdpcap("tests/homomorphic_encryption/noTLS.pcap")

    result = Communication.PETValidation(packets)

    assert result["Use TLS v1.2 or later"] is False

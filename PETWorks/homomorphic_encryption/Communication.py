import scapy.all
from scapy.plist import PacketList

scapy.all.load_layer("tls")


def capturePackets(timeout: int, interface: str) -> PacketList:
    if timeout is None:
        timeout = 5  # Sniff for 5 seconds

    packets = scapy.all.sniff(timeout=timeout, iface=interface)
    return packets


def PETValidation(packets):
    tlsPackets = (
        packet
        for packet in packets
        if packet.haslayer("TLS") and packet["TLS"].version >= 0x0303
    )

    return {"Use TLS v1.2 or later": any(tlsPackets)}

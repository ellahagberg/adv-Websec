from scapy.all import rdpcap, IP
import sys


def ip_to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) + (b << 16) + (c << 8) + d


def load_ip_pairs(pcap_file):
    pairs = []
    for pkt in rdpcap(pcap_file):
        if IP in pkt:
            pairs.append((pkt[IP].src, pkt[IP].dst))
    return pairs


#blev chill
def disclosure_attack(nazir_ip, mix_ip, m, pcap_file):
    pairs = load_ip_pairs(pcap_file)

    batches = []
    current_receivers = set()
    nazir_active = False
    output_phase = False

    for src, dst in pairs:
        
        if dst == mix_ip and src != mix_ip:
            if output_phase:
               
                if nazir_active:
                    batches.append(current_receivers)
                current_receivers = set()
                nazir_active = False
                output_phase = False

            if src == nazir_ip:
                nazir_active = True

        elif src == mix_ip:
            output_phase = True
            current_receivers.add(dst)

   
    if nazir_active:
        batches.append(current_receivers)

  
    saved = []
    for R in batches:
        if all(R.isdisjoint(S) for S in saved):
            saved.append(set(R))
        if len(saved) == m:
            break

   
    for R in batches:
        hits = [i for i, S in enumerate(saved) if (R & S)]
        if len(hits) == 1:
            i = hits[0]
            saved[i] = saved[i] & R

    
    partners = [next(iter(S)) for S in saved]
    return sum(ip_to_int(ip) for ip in partners)


#command för att köra: python3 M3P2.py 61.152.13.37 95.235.155.122 8 cia.log.3.pcap
# sen cd gunzip -k cia.log.3.pcap.gz för pcap
if __name__ == "__main__":
    nazir_ip = sys.argv[1]
    mix_ip = sys.argv[2]
    m = int(sys.argv[3])
    pcap_file = sys.argv[4]

    print(disclosure_attack(nazir_ip, mix_ip, m, pcap_file))
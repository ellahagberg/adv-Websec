import hashlib
import json
import time
import urllib.request
import urllib.parse

SERVER = "http://igor.eit.lth.se:6003"

def sha256_hex(s: str):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def now_timestamp():
    return time.strftime("%Y-%m-%d, %H:%M:%S")

def http_get(url: str):
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")

#steg1
def mine_block(seed: str, block_id: int, prev_hash: str, metadata: str):
    ts = now_timestamp()
    nonce = 0
    while True:
        payload = f"{block_id}-{ts}-{metadata}-{prev_hash}-{nonce}"
        curr_hash = sha256_hex(payload)
        if curr_hash.startswith(seed):
            return {
                "block_id": block_id,
                "time_stamp": ts,
                "metadata": metadata,
                "prev_hash": prev_hash,
                "nonce": nonce,
                "curr_hash": curr_hash,
            }
        nonce += 1

def main():
    #steg2 för qiuz
    seed = "cccc" 

    
    gen_url = f"{SERVER}/generate?seed={seed}"
    bc_text = http_get(gen_url)
    
    #fixade så man bara tar json i pure inte html
    json_start = bc_text.find('[{')  #kanske kunde göras enklare, men blev en quick fix för extraction
    json_end = bc_text.rfind(']') + 1
    json_str = bc_text[json_start:json_end]
    
    chain = json.loads(json_str)  #steg3 hämta med json.loads

    #steg4 mine:a tre block till
    while len(chain) < 5:
        prev = chain[-1]
        new_id = prev["block_id"] + 1
        new_block = mine_block(
            seed=seed,
            block_id=new_id,
            prev_hash=prev["curr_hash"],
            metadata=f"block{new_id}",
        )
        chain.append(new_block)

    #steg5 använder json.dumps
    chain_json = json.dumps(chain, separators=(",", ":"))  
    chain_param = urllib.parse.quote(chain_json, safe="")
    submit_url = f"{SERVER}/submit?seed={seed}&chain={chain_param}"

    result = http_get(submit_url)
    print(result)

if __name__ == "__main__":
    main()

def extract_vip_list(data):
    """
    あなたの環境の VIP API は以下の構造:
    {
      "vip": {
        "vip": {
          "UUID1": {...},
          "UUID2": {...}
        }
      }
    }

    → 各エントリに uuid を埋め込んで list に変換する
    """
    if "vip" not in data:
        raise AssertionError(f"Invalid VIP response: {data}")

    vip_section = data["vip"]

    if isinstance(vip_section, dict) and "vip" in vip_section:
        inner = vip_section["vip"]

        if isinstance(inner, dict):
            result = []
            for uuid_key, item in inner.items():
                entry = dict(item)
                entry["uuid"] = uuid_key
                result.append(entry)
            return result

        if isinstance(inner, list):
            return inner

    raise AssertionError(f"Unexpected VIP structure: {vip_section}")


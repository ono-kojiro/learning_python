# file: src/amcli/commands/generate_schema/through_model.py

def collect_through_models(models):
    through_models = []

    for model_name, model_def in models.items():
        fields = model_def.get("fields", {})
        for field_name, field_def in fields.items():

            ftype = field_def.get("type")

            if ftype in ("many_to_many", "ManyToMany", "ManyToManyField"):
                to_model = field_def.get("to")
                through_name = f"{model_name}{to_model}"

                # ★ 追加：辞書順で小さい方だけ採用
                if model_name < to_model:
                    through_models.append({
                        "name": through_name,
                        "from": model_name,
                        "to": to_model,
                        "field": field_name,
                    })

    return through_models

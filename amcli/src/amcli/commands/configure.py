# amcli/commands/configure.py

import os
from glob import glob


def run(output_file, application, project):
    """
    Generate build.ninja exactly matching the reference build.ninja.
    """

    # ----------------------------------------
    # 固定の spec 順序（reference と完全一致）
    # ----------------------------------------
    spec_order = [
        "device",
        "netif",
        "ipv4",
        "comment",
        "manager",
        "remark",
        "os",
    ]

    specs = [f"specs/{name}.yml" for name in spec_order]
    spec_jsons = [f"work/specs/{name}.json" for name in spec_order]

    # importer templates
    importer_map = {
        "urls_api.py": "template/urls.j2",
        "loader.py": "template/loader.j2",
        "apps.py": "template/apps.py.j2",
        "models/__init__.py": "template/models_init.j2",
    }

    # ----------------------------------------
    # build.ninja の生成開始
    # ----------------------------------------
    lines = []

    # ----------------------------------------
    # rules（reference と完全一致）
    # ----------------------------------------
    lines += [
        "###############################################",
        "# rules",
        "###############################################",
        "",
        "rule startproject",
        f"  command = amcli startproject {project} --dir work/",
        "",
        "rule startapp",
        f"  command = amcli startapp {application} --dir work/",
        "",
        "rule installapp_export",
        f"  command = amcli installapp --export-installed-apps work/{project}/installed_apps.yml --project work/{project}/",
        "",
        "rule installapp_replace",
        f"  command = amcli installapp --replace-installed-apps work/{project}/installed_apps.yml --project work/{project}/",
        "",
        "rule installapp_pkg",
        f"  command = amcli installapp $pkg --project work/{project}/",
        "",
        "rule mkdir",
        "  command = mkdir -p $dir",
        "",
        "rule allowed_hosts_export",
        f"  command = amcli edit --export work/{project}/allowed_hosts.yml --project work/{project} ALLOWED_HOSTS",
        "",
        "rule allowed_hosts_write",
        f"  command = echo \"[ \\\"*\\\" ]\" > work/{project}/allowed_hosts.yml",
        "",
        "rule allowed_hosts_import",
        f"  command = amcli edit --import work/{project}/allowed_hosts.yml --project work/{project} ALLOWED_HOSTS",
        "",
        "rule patch_urls",
        "  command = sh patch_urls.sh",
        "",
        "",
        "###############################################",
        "# targets (依存関係つき)",
        "###############################################",
        "",
        "# 1. startproject",
        "build work/.startproject: startproject",
        "",
        "# 2. startapp（startproject 完了後）",
        "build work/.startapp: startapp work/.startproject",
        "",
        "# 3. installapp export（startapp 完了後）",
        "build work/.installapp_export: installapp_export work/.startapp",
        "",
        "# 4. installapp replace（export 完了後）",
        "build work/.installapp_replace: installapp_replace work/.installapp_export",
        "",
        "# 5. installapp rest_framework（replace 完了後）",
        "build work/.installapp_rest: installapp_pkg work/.installapp_replace",
        "  pkg = rest_framework",
        "",
        "# 6. installapp django_extensions",
        "build work/.installapp_ext: installapp_pkg work/.installapp_rest",
        "  pkg = django_extensions",
        "",
        "# 7. installapp myapp",
        "build work/.installapp_myapp: installapp_pkg work/.installapp_ext",
        f"  pkg = {application}",
        "",
        "# 8. mkdir 群（myapp インストール後）",
        "build work/.mkdir_specs: mkdir work/.installapp_myapp",
        "  dir = work/specs",
        "",
        "build work/.mkdir_models: mkdir work/.installapp_myapp",
        f"  dir = work/{application}/models",
        "",
        "build work/.mkdir_views: mkdir work/.installapp_myapp",
        f"  dir = work/{application}/views",
        "",
        "build work/.mkdir_serializers: mkdir work/.installapp_myapp",
        f"  dir = work/{application}/serializers",
        "",
        "build work/.mkdir_schema: mkdir work/.installapp_myapp",
        "  dir = work/schema",
        "",
        "build work/.mkdir_tests: mkdir work/.installapp_myapp",
        "  dir = tests/data",
        "",
        "# 9. allowed_hosts export",
        "build work/.allowed_hosts_export: allowed_hosts_export work/.mkdir_schema",
        "",
        "# 10. allowed_hosts write",
        "build work/.allowed_hosts_write: allowed_hosts_write work/.allowed_hosts_export",
        "",
        "# 11. allowed_hosts import",
        "build work/.allowed_hosts_import: allowed_hosts_import work/.allowed_hosts_write",
        "",
        "# 12. urls.py patch",
        "build work/.patch_urls: patch_urls work/.allowed_hosts_import",
        "",
        "",
        "###############################################",
        "# final target",
        "###############################################",
        "",
        "build init: phony work/.startproject work/.startapp work/.installapp_export work/.installapp_replace work/.installapp_rest work/.installapp_ext work/.installapp_myapp work/.mkdir_specs work/.mkdir_models work/.mkdir_views work/.mkdir_serializers work/.mkdir_schema work/.mkdir_tests work/.allowed_hosts_export work/.allowed_hosts_write work/.allowed_hosts_import work/.patch_urls",
        "",
        "",
        "rule cmp2ref",
        "  command = amcli cmp2ref --spec $in -o $out " + " ".join(specs),
        "",
    ]

    # ----------------------------------------
    # cmp2ref build lines
    # ----------------------------------------
    for name in spec_order:
        lines.append(f"build work/specs/{name}.json:   cmp2ref specs/{name}.yml   | init")
    lines.append("")

    # ----------------------------------------
    # genschema
    # ----------------------------------------
    lines += [
        "rule genschema",
        f"  command = amcli genschema -o $out --project {project} --application {application} "
        + " ".join(spec_jsons),
        "",
        "build work/schema/schema.json: genschema " + " ".join(spec_jsons),
        "",
        "",
        "",
    ]

    # ----------------------------------------
    # genmodel
    # ----------------------------------------
    lines += [
        "rule genmodel",
        "  command = amcli genmodel -l template -o $out $in",
        "",
    ]
    for name in spec_order:
        lines.append(f"build work/{application}/models/{name}_model.py:   genmodel work/specs/{name}.json")
    lines.append("")

    # ----------------------------------------
    # genadmin
    # ----------------------------------------
    lines += [
        "rule genadmin",
        "  command = amcli genadmin -o $out -l template -s work/schema/schema.json $in",
        "",
    ]
    for name in spec_order:
        lines.append(f"build work/{application}/admin/{name}_admin.py:   genadmin work/specs/{name}.json")
    lines.append("")

    # ----------------------------------------
    # genview
    # ----------------------------------------
    lines += [
        "rule genview",
        "  command = amcli genview -o $out -l template $in",
        "",
    ]
    for name in spec_order:
        lines.append(f"build work/{application}/views/{name}_view.py:   genview work/specs/{name}.json")
    lines.append("")

    # ----------------------------------------
    # genserializer
    # ----------------------------------------
    lines += [
        "rule genserializer",
        "  command = amcli genserializer -o $out -l template -s work/schema/schema.json $in",
        "",
    ]
    for name in spec_order:
        lines.append(f"build work/{application}/serializers/{name}_serializer.py:   genserializer work/specs/{name}.json")
    lines.append("")

    # ----------------------------------------
    # genfixture
    # ----------------------------------------
    lines += [
        "rule genfixture",
        "  command = amcli genfixture -o $out -l template -s work/schema/schema.json -n template/names.yaml $in",
        "",
    ]
    for name in spec_order:
        lines.append(f"build tests/data/test_{name}-fixtures.yaml:   genfixture work/specs/{name}.json")
    lines.append("")

    # ----------------------------------------
    # genimporter
    # ----------------------------------------
    lines += [
        "rule genimporter",
        "  command = amcli genimporter -o $out -s work/schema/schema.json $in",
        "",
    ]
    for out, tmpl in importer_map.items():
        lines.append(f"build work/{application}/{out}:        genimporter {tmpl}")
    lines.append("")

    # ----------------------------------------
    # rmdb / makemigrations / migrate / loaddata
    # ----------------------------------------
    lines += [
        "",
        "rule rmdb",
        "  command = rm -f work/db.sqlite3",
        "rule makemigrations",
        "  command = cd work && python3 manage.py makemigrations && cd ..",
        "",
        "rule migrate",
        "  command = cd work && python3 manage.py migrate && cd ..",
        "rule createsuperuser",
        "  command = sh createsuperuser.sh",
        "",
        "rule loaddata",
        "  command = python3 work/manage.py loaddata $in",
        "",
        "build work/.rmdb: rmdb work/schema/schema.json",
        "",
        "",
        "rule touch",
        "  command = touch $out",
        f"build work/{application}/admin/__init__.py: touch work/.installapp_myapp",
        f"build work/{application}/views/__init__.py: touch work/.installapp_myapp",
        "",
    ]

    # ----------------------------------------
    # makemigrations（reference と完全一致）
    # ----------------------------------------
    makemig = [
        f"work/{application}/urls_api.py",
        f"work/{application}/loader.py",
        f"work/{application}/apps.py",
        f"work/{application}/models/__init__.py",
    ]

    makemig += [f"work/{application}/models/{name}_model.py" for name in spec_order]
    makemig += [f"work/{application}/admin/{name}_admin.py" for name in spec_order]
    makemig += [f"work/{application}/views/{name}_view.py" for name in spec_order]
    makemig += [f"work/{application}/serializers/{name}_serializer.py" for name in spec_order]

    makemig += [
        f"work/{application}/admin/__init__.py",
        f"work/{application}/views/__init__.py",
        "work/.rmdb",
    ]

    lines.append("build work/.makemigrations: makemigrations " + " ".join(makemig))
    lines.append("")

    # ----------------------------------------
    # migrate → createsuperuser → loaddata
    # ----------------------------------------
    lines.append("build work/.migrate: migrate work/.makemigrations")
    lines.append("build work/.createsuperuser: createsuperuser work/.migrate")
    lines.append("")

    fixtures = [f"tests/data/test_{name}-fixtures.yaml" for name in spec_order]
    lines.append("build work/.loaddata: loaddata " + " ".join(fixtures))
    lines.append("")

    # ----------------------------------------
    # write build.ninja
    # ----------------------------------------
    with open(output_file, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated {output_file}")

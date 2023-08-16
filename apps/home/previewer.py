from flask import render_template
from flask_login import current_user


def previewer(token: str, file_list: list):
    file_id = file_list[0]

    contentSidebarProps = {
        "detailsSidebarProps": {
            "hasNotices": True,
            "hasProperties": True,
            "hasAccessStats": True,
            "hasVersions": True,
        },
        "hasActivityFeed": True,
        "hasSkills": True,
        "hasVersions": True,
        "hasMetadata": True,
    }

    options = {
        "container": ".ui-element",
        "header": "light",
        # "logoUrl": "box",
        "collection": file_list,
        "hasHeader": True,
        "showAnnotations": False,
        "showDownload": True,
        "contentSidebarProps": contentSidebarProps,
    }

    isSingle = True if file_list.count == 1 else False

    return render_template(
        "home/previewer.html",
        segment="previewer",
        avatar_url=current_user.avatar_url,
        token=token,
        file_id=file_id,
        options=options,
        isSingle=isSingle,
    )

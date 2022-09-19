from typegraph.graphs.typegraph import github_auth
from typegraph.graphs.typegraph import Rate
from typegraph.graphs.typegraph import TypeGraph
from typegraph.materializers.deno import ModuleMat
from typegraph.policies import allow_all
from typegraph.types import typedefs as t


def send_in_blue_send(subject, frm, to, api_key):
    f = ModuleMat("send_in_blue_send.ts")

    return t.func(
        t.struct(
            {
                "name": t.string(),
                "email": t.email(),
                "subject": t.string().s_raw(subject),
                "message": t.string(),
                "apiKey": t.string().s_secret(api_key),
                "from": t.string().s_secret(frm),
                "to": t.string().s_secret(to),
            }
        ),
        t.struct({"success": t.boolean(), "error": t.string().s_optional()}),
        f.imp("default"),
    ).rate(weight=2)


with TypeGraph(
    "biscuicuits",
    auths=[github_auth],
    rate=Rate(window_limit=2000, window_sec=60, query_limit=200),
) as g:

    all = allow_all()

    g.expose(
        contact=send_in_blue_send(
            "Nouveau message",
            "SENDER",
            "TO",
            "SENDINBLUE_API_KEY",
        ).add_policy(all)
    )
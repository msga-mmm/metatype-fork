// Copyright Metatype OÜ, licensed under the Elastic License 2.0.
// SPDX-License-Identifier: Elastic-2.0

import { Policy, t, typegraph } from "@typegraph/deno/src/mod.ts";
import { PythonRuntime } from "@typegraph/deno/src/runtimes/python.ts";
import outdent from "outdent";

const tpe = t.struct({
  "a": t.string(),
  "b": t.array(t.either([t.integer(), t.string()])),
});

typegraph("python_wasi", (g) => {
  const python = new PythonRuntime();
  const pub = Policy.public();

  g.expose({
    identityLambda: python.fromLambda(
      t.struct({ input: tpe }),
      tpe,
      { code: "lambda x: x['input']" },
    ).withPolicy(pub),
    identityDef: python.fromDef(
      t.struct({ input: tpe }),
      tpe,
      {
        code: outdent`
        def identity(x):
          return x['input']
        `,
      },
    ).withPolicy(pub),
    identityMod: python.import(
      t.struct({ input: tpe }),
      tpe,
      { name: "identity", module: "py/hello.py" },
    ).withPolicy(pub),
  });
});

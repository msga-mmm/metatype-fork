// Copyright Metatype OÜ, licensed under the Mozilla Public License Version 2.0.
// SPDX-License-Identifier: MPL-2.0

use crate::{
    errors::Result,
    t::{self, ConcreteTypeBuilder, TypeBuilder},
    types::TypeId,
};

use super::{TypeGen, TypeGenContext};

pub struct Count;

impl TypeGen for Count {
    fn generate(&self, context: &mut TypeGenContext) -> Result<TypeId> {
        t::optional(t::integer().build()?)
            .named(self.name(context))
            .build()
    }

    fn name(&self, _context: &TypeGenContext) -> String {
        "_Count".to_string()
    }
}
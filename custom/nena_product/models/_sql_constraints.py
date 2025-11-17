_sql_constraints = [
        (
            "code_description_unique",
            "UNIQUE(code,name_subtype,nena_product_class_id)",
            "El código de la clase del producto debe de ser único",
        )
    ]
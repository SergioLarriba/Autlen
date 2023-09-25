
    def test_exercise_0(self) -> None:
        self.check_expression(RE0, "a", True)
        self.check_expression(RE0, "bbbbaba", True)
        self.check_expression(RE0, "abbab", False)
        self.check_expression(RE0, "b", False)
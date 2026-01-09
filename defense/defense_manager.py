class DefenseManager(BaseManager):
    def __init__(self, context=None, local_bus=None):
        super().__init__(context=context)
        self.local_bus = local_bus

    def update(self, entity_data):
        pass

    @property
    def state(self) -> ComponentUpgradeState:
        if all(
            [
                self.db_creation_state == OperationState.SUCCESS,
                self.db_refresh_state == OperationState.SUCCESS,
                self.secret_update_state == OperationState.SUCCESS,
                self.kube_restart_state == OperationState.SUCCESS,
            ]
        ):
            state = ComponentUpgradeState.UPGRADED
        elif any(
            [
                self.db_creation_state == OperationState.FAILED,
                self.db_refresh_state == OperationState.FAILED,
                self.secret_update_state == OperationState.FAILED,
                self.kube_restart_state == OperationState.FAILED,
            ]
        ):
            state = ComponentUpgradeState.UPGRADE_FAILED
        elif all(
            [
                self.db_creation_state == OperationState.PENDING,
                self.db_refresh_state == OperationState.PENDING,
                self.secret_update_state == OperationState.PENDING,
                self.kube_restart_state == OperationState.PENDING,
            ]
        ):
            state = ComponentUpgradeState.UPGRADING
        else:
            state = ComponentUpgradeState.UPGRADE_REQUESTED

        return state

    def _refresh_cluster_upgrade_step(
        self, cluster_upgrade: DataplaneClusterUpgrade
    ) -> DataplaneClusterUpgrade:
        cluster = self.repositories.dataplane_cluster.get_by_id(
            cluster_upgrade.new_dataplane_cluster_id
        )
        if (
            self._new_cluster_is_active(cluster.id)
            and cluster_upgrade.upgrade_step != DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATED
        ):
            self._update_cluster_upgrade_with(
                cluster_upgrade,
                upgrade_step=DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATED,
            )
        if (
            cluster.status == Status.CREATING
            and cluster_upgrade.upgrade_step != DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATING
        ):
            self._update_cluster_upgrade_with(
                cluster_upgrade,
                upgrade_step=DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATING,
            )
        if (
            cluster.status == Status.FAILED
            and cluster_upgrade.upgrade_step
            != DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATION_FAILED
        ):
            self._update_cluster_upgrade_with(
                cluster_upgrade,
                upgrade_step=DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATION_FAILED,
            )

        return self.repositories.dataplane_cluster_upgrade.get_by_id(cluster_upgrade.id)

def _refresh_cluster_upgrade_step(
    self, cluster_upgrade: DataplaneClusterUpgrade
) -> DataplaneClusterUpgrade:
    cluster = self.repositories.dataplane_cluster.get_by_id(
        cluster_upgrade.new_dataplane_cluster_id
    )

    new_upgrade_step = None

    if self._new_cluster_is_active(cluster.id):
        new_upgrade_step = DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATED

    if cluster.status == Status.CREATING:
        new_upgrade_step = DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATING

    if cluster.status == Status.FAILED:
        new_upgrade_step = DataplaneClusterUpgradeStep.NEW_CLUSTER_CREATION_FAILED

    if (
        new_upgrade_step
        and cluster_upgrade.upgrade_step != new_upgrade_step
    ):
        self._update_cluster_upgrade_with(
            cluster_upgrade,
            upgrade_step=new_upgrade_step,
        )

    return self.repositories.dataplane_cluster_upgrade.get_by_id(cluster_upgrade.id)

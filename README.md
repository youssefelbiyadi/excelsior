# excelsior

set step attr to SOME_STEP when operation_x is executed succesfuly
_operation_x uses OperationStateManager taht sets the operation_x_state to PENDING
when entering context manage, to SUCCES if create_or_manage_model_resource is executed 
without errors, and FAILED if an exception is raised.
create_or_manage_model_resource is be named differently (like operation x)
depending on the operation of the workflow, it is used to create or manage the external resource
concerned by the step.
in my real workflow i have 4 operations in this order:
- create_cluster
_ create_database 
_ refresh_from_old_database
_ stop_old_sluster

the workflow is used to upgrade a created postgres cluster to a newer version, by creating a new one with specified version.
the model will be an instance of ClusterUpgrade model, and states are:
- cluster_creation_state
_ db_creation_state 
_ db_refresh_state
_ stopping_old_cluster_state

and the steps are CLUSTER_CREATION, DB_CREATION, DB_REFRESH, CLUSTER_STOP

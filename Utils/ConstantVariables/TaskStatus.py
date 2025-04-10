class TaskStatus:
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    CANCELED = 3

    CHOICES = {
        PENDING: "Pending",
        IN_PROGRESS: "In Progress",
        COMPLETED: "Completed",
        CANCELED: "Canceled",
    }

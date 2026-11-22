
/**
 * Google Tasks → Google Calendar Sync
 *
 * Creates all-day calendar events for tasks with due dates.
 * Uses task IDs to prevent duplicate events.
 * Updates events when task details change.
 */

const CONFIG = {
  CALENDAR_ID: 'primary',
  EVENT_PREFIX: '[Task] ',
  INCLUDE_COMPLETED: false,
  DAYS_TO_SYNC: 365
};

function syncTasksToCalendar() {
  const calendar = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID);
  const properties = PropertiesService.getScriptProperties();

  if (!calendar) {
    throw new Error('Calendar not found.');
  }

  // Retrieve all Google Tasks lists
  const taskLists = Tasks.Tasklists.list().items || [];

  taskLists.forEach(taskList => {
    let pageToken;

    do {
      const response = Tasks.Tasks.list(taskList.id, {
        showCompleted: CONFIG.INCLUDE_COMPLETED,
        showDeleted: false,
        maxResults: 100,
        pageToken: pageToken
      });

      const tasks = response.items || [];

      tasks.forEach(task => {
        if (!task.due) return;
        if (task.status === 'completed' && !CONFIG.INCLUDE_COMPLETED) return;

        const taskDate = new Date(task.due);
        const dateKey = Utilities.formatDate(
          taskDate,
          Session.getScriptTimeZone(),
          'yyyy-MM-dd'
        );

        const propertyKey = 'task_' + task.id;
        const existingEventId = properties.getProperty(propertyKey);

        const title = CONFIG.EVENT_PREFIX + task.title;
        const description = [
          task.notes || '',
          '',
          'Google Tasks list: ' + taskList.title,
          'Task ID: ' + task.id
        ].join('\n');

        let event = existingEventId
          ? calendar.getEventById(existingEventId)
          : null;

        // Update existing event
        if (event) {
          event.setTitle(title);
          event.setDescription(description);

          const existingDate = Utilities.formatDate(
            event.getAllDayStartDate(),
            Session.getScriptTimeZone(),
            'yyyy-MM-dd'
          );

          if (existingDate !== dateKey) {
            event.setAllDayDate(taskDate);
          }

        } else {
          // Create a new all-day event
          event = calendar.createAllDayEvent(
            title,
            taskDate,
            { description: description }
          );

          properties.setProperty(propertyKey, event.getId());
        }
      });

      pageToken = response.nextPageToken;

    } while (pageToken);
  });
}

/**
 * Executes every 15 minutes.
 */
function installTrigger() {
  // Prevent duplicate triggers
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === 'syncTasksToCalendar') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  ScriptApp.newTrigger('syncTasksToCalendar')
    .timeBased()
    .everyMinutes(15)
    .create();
}

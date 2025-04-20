{/* <Cards
  name="Ожидание"
  style="expecting-color"
  type="progress"
  // data={progress}
/> */}

export const filtratedTasksExpecting = state => {
  return state.tasks.filter(task => {
    return task.type === "Ожидание";
  });
};

export const filtratedTasksReadySawing = state => {
  return state.tasks.filter(task => {
    return task.type === "Готов к распилу";
  });
};

export const filtratedTasksSawed = state => {
  return state.tasks.filter(task => {
    return task.type === "Пилится";
  });
};

export const filtratedTasksAwaitingAssembly = state => {
  return state.tasks.filter(task => {
    return task.type === "Ожидает сборку";
  });
};

export const filtratedTasksKarskasIsGoing = state => {
  return state.tasks.filter(task => {
    return task.type === "Карскас собирается";
  });
};



export const filtratedTasksBacklog = state => {
  return state.tasks.filter(task => {
    return task.type === "backlog";
  });
};

export const filtratedTasksProgress = state => {
  return state.tasks.filter(task => {
    return task.type === "progress";
  });
};

export const filtratedTasksReview = state => {
  return state.tasks.filter(task => {
    return task.type === "review";
  });
};

export const filtratedTasksComplete = state => {
  return state.tasks.filter(task => {
    return task.type === "complete";
  });
};

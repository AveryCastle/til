export const add = (a, b) => {
  return (a || 0) + (b || 0);
};

export const add1 = (...numbers) => numbers.reduce((accumulator, currentValue) => accumulator + (currentValue || 0), 0);
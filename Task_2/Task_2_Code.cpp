#include <iostream>

int wayOfRising(int *arr, int steps) {
	if (arr[steps - 1] >= 0) {
		//std::cout << steps << "´Ü : " << arr[steps - 1] << std::endl;
		return arr[steps - 1];
	}
	else {
		arr[steps - 1] = wayOfRising(arr, steps - 1) + wayOfRising(arr, steps - 2);
		//std::cout << steps << "´Ü : " << arr[steps - 1] << std::endl;
		return arr[steps - 1];
	}
}

int main() {
	int n, a, b;
	int step[30];
	std::fill_n(step, 30, -1);
	step[0] = 1;
	step[1] = 2;
	std::cin >> n >> a >> b;
	if (a != 0)
		step[a - 1] = 0;
	if (b != 0)
		step[b - 1] = 0;
	if (step[0] == 0 && step[1] != 0)
		step[1] = 1;
	std::cout << wayOfRising(step, n) << std::endl;
}
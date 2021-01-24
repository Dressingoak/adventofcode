#include <array>

#include <spdlog/spdlog.h>
#include <spdlog/stopwatch.h>

#include "ETA.h"
#include "CrabCups.h"

int main() {

	spdlog::set_level(spdlog::level::info);
	spdlog::info("Initializing...");
	spdlog::stopwatch sw;
	auto cc = CrabCups<unsigned, 9, 1000000>("871369452");
	spdlog::info("Initialized in {:.3}", sw);
	spdlog::info("Starting...");
	spdlog::stopwatch sw2;

	constexpr unsigned swaps = 10000000U;
	constexpr unsigned log_every = 10000U;
	constexpr unsigned outer = swaps / log_every;
	ETA<outer> eta;
	for (unsigned i = 1; i <= outer; i++)
	{
		for (unsigned j = 0; j < log_every; j++)
			cc.move();
		eta.update(sw2.elapsed(), i);
		spdlog::info("Progress: {:>5.1f}% (ETA: {})", eta.get_percentage(), eta);
	}
	spdlog::info("Completed in {:.3}", sw2);
	auto of1 = cc.find(1, 1);
	auto of2 = cc.find(1, 2);
	spdlog::info("Clock-wise of 1 we have {} and {}", of1, of2);
	spdlog::info("Part 2: {}", of1 * of2);

}

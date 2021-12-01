#pragma once
#include <iostream>
#include <iomanip>
#include <chrono>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

template<std::size_t T>
class ETA
{
	using SECONDS = std::chrono::duration<double>;

	std::size_t completed = 0;
	double progress = 0.0;
	SECONDS elapsed{ 0.0 };
public:
	ETA() = default;

	void update(std::chrono::duration<double> _elapsed, std::size_t _completed)
	{
		completed = _completed;
		elapsed = _elapsed;
		progress = (double)completed / (double)T;
	}

	double get_percentage() const
	{
		return progress * 100.0;
	}

	SECONDS get_remaining() const
	{
		double e = elapsed.count();
		return SECONDS(e / progress - e);
	}
};

template<std::size_t T>
inline std::ostream& operator<<(std::ostream& os, const ETA<T>& eta)
{
	auto s = eta.get_remaining();
	typedef std::chrono::duration<int, std::ratio<86400>> days;
	char fill = os.fill();
	os.fill('0');
	auto d = std::chrono::duration_cast<days>(s);
	s -= d;
	auto h = std::chrono::duration_cast<std::chrono::hours>(s);
	s -= h;
	auto m = std::chrono::duration_cast<std::chrono::minutes>(s);
	s -= m;
	auto sx = std::chrono::duration_cast<std::chrono::seconds>(s);
	os << std::setw(2) << d.count() << "d:"
		<< std::setw(2) << h.count() << "h:"
		<< std::setw(2) << m.count() << "m:"
		<< std::setw(2) << sx.count() << 's';
	os.fill(fill);
	return os;
}

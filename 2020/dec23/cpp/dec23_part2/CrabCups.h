#pragma once
#include <map>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

template<std::size_t N, std::size_t M = N>
class CrabCups {
	using T = typename unsigned;
	using Map = typename std::map<T, T>;

private:
	unsigned int _moves = 0;
	const std::size_t _swapped = 3;
	bool _formatted = true;
	T _current;
	Map _data;

private:
	static T char2uint(const char c) { return c - '0'; }

public:
	CrabCups(const char(&data)[N + 1])
		: _current(char2uint(data[0]))
	{
		auto get_value = [&data](std::size_t i) {
			T idx = i % M;
			if (idx < N)
				return char2uint(data[idx]);
			else
				return idx + 1;
		};
		for (std::size_t i = 0; i < M; i++)
		{
			T value = get_value(i);
			T next = get_value(i + 1);
			_data[value] = next;
		}
	}

	constexpr T size() const {
		return M;
	}

	unsigned int get_moves() const {
		return _moves;
	}

public:
	void set_formatted(bool value) { _formatted = value; }
	bool is_formatted() const { return _formatted; }

	T get_current() const { return _current; }

	T follow(const T value, const T n) const
	{
		T cur = value;
		for (T i = 0; i < n; i++)
			cur = _data.at(cur);
		return cur;
	}

	static constexpr T subtract(T value)
	{
		return value == 1 ? M : value - 1;
	}

	T get_destination() const {
		T target = subtract(_current);
		for (unsigned i = 0; i < _swapped; i++)
		{
			bool appeared = false;
			T tail = _data.at(_current);
			for (unsigned j = 0; j < _swapped; j++)
			{
				if (tail == target)
				{
					// spdlog::trace("Cannot be that!");
					appeared = true;
					break;
				}
				tail = _data.at(tail);
			}
			if (!appeared)
				break;
			else
				target = subtract(target);
		}
		return target;
	}

private:

	void swap_cups()
	{
		T destination = get_destination();
		// spdlog::trace("destination is {}", destination);

		T segment_end = follow(_current, _swapped);
		// spdlog::trace("segment_end is {}", segment_end);

		T after_current = _data.at(segment_end);
		// spdlog::trace("after_current is {}", after_current);

		T after_destination = _data.at(_current);
		// spdlog::trace("after_destination is {}", after_destination);

		T after_segment = _data.at(destination);
		// spdlog::trace("after_segment is {}", after_segment);
		

		_data[_current] = after_current;
		_data[destination] = after_destination;
		_data[segment_end] = after_segment;

		_current = _data.at(_current);
	}

public:
	void move() {
		_moves++;
		swap_cups();
	}

	void move_detailed()
	{
		spdlog::debug("-- move {}--", _moves + 1);
		spdlog::debug("cups: {}", *this);
		spdlog::debug("pick up: {}, {}, {}", follow(_current, 1), follow(_current, 2), follow(_current, 3));
		spdlog::debug("destination: {}", get_destination());
		move();
	}

	std::ostream& print_simple(std::ostream& os, const T start = 1, unsigned cut = 0) const
	{
		auto value = start;
		for (std::size_t i = 0; i < M - cut; i++)
		{
			value = _data.at(value);
			os << value;
		}
		return os;
	}

	std::ostream& print_formatted(std::ostream& os) const
	{
		auto dist = M - _moves % M;
		const std::size_t init = follow(get_current(), dist);
		std::size_t value = init;
		do {
			if (value == get_current())
				os << "(" << value << ")";
			else
				os << " " << value << " ";
			auto next = _data.at(value);
			value = next;
		} while (value != init);
		return os;
	}

};

template<std::size_t N, std::size_t M>
inline std::ostream& operator<<(std::ostream& os, const CrabCups<N, M>& cc)
{
	if (cc.is_formatted())
		return cc.print_formatted(os);
	else
		return cc.print_simple(os, 1, 1);
}

template<std::size_t N>
CrabCups(const char(&data)[N])->CrabCups<N - 1>;

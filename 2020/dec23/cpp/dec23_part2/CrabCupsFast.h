#pragma once
#include <vector>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

template<std::size_t N, std::size_t M = N>
class CrabCups {
	using T = typename unsigned;
	using Vect = typename std::vector<T>;

private:
	unsigned int _moves = 0;
	const std::size_t _swapped = 3;
	bool _formatted = true;
	T _current;
	Vect _data;

private:
	static T char2uint(const char c) { return c - '0'; }
	static char uint2char(const T u) { return '0' + u; }

	static T get_position(const char* data, const char c)
	{
		auto p = strchr(data, c);
		return p - data;
	}

public:
	CrabCups(const char(&data)[N + 1])
		: _current(char2uint(data[0]) - 1)
	{
		_data.reserve(M);
		auto get_value = [&data](std::size_t i) {
			T idx = i % M;
			if (idx < N)
				return char2uint(data[idx]) - 1;
			else
				return idx;
		};
		for (std::size_t i = 0; i < N; i++)
		{
			auto pos = get_position(data, uint2char(i + 1));
			_data.push_back(get_value(pos + 1));
		}
		for (std::size_t i = N; i < M; i++)
		{
			_data.push_back(get_value(i + 1));
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

private:
	T get_current_internal() const { return _current; }
public:
	T get_current() const { return _current + 1; }

private:
	T follow_internal(const T value, const T n) const
	{
		T cur = value;
		for (T i = 0; i < n; i++)
			cur = _data[cur];
		return cur;
	}
public:
	T follow(const T value, const T n) const { return follow_internal(value - 1, n) + 1; }

	static constexpr T subtract(T value)
	{
		return value == 0 ? M - 1 : value - 1;
	}

private:
	T get_destination_internal() const {
		T target = subtract(_current);
		for (unsigned i = 0; i < _swapped; i++)
		{
			bool appeared = false;
			T tail = _data[_current];
			for (unsigned j = 0; j < _swapped; j++)
			{
				if (tail == target)
				{
					appeared = true;
					break;
				}
				tail = _data[tail];
			}
			if (!appeared)
				break;
			else
				target = subtract(target);
		}
		return target;
	}
	T get_destination() const {
		return get_destination_internal() + 1;
	}

private:

	void swap_cups()
	{
		T destination = get_destination_internal();
		// spdlog::trace("destination is {}", destination);

		T segment_end = follow_internal(_current, _swapped);
		// spdlog::trace("segment_end is {}", segment_end);

		T after_current = _data[segment_end];
		// spdlog::trace("after_current is {}", after_current);

		T after_destination = _data[_current];
		// spdlog::trace("after_destination is {}", after_destination);

		T after_segment = _data[destination];
		// spdlog::trace("after_segment is {}", after_segment);
		

		_data[_current] = after_current;
		_data[destination] = after_destination;
		_data[segment_end] = after_segment;

		_current = _data[_current];
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
		spdlog::debug("pick up: {}, {}, {}", follow_internal(_current, 1) + 1, follow_internal(_current, 2) + 1, follow_internal(_current, 3) + 1);
		spdlog::debug("destination: {}", get_destination());
		move();
	}

	std::ostream& print_simple(std::ostream& os, const T start = 0, unsigned cut = 0) const
	{
		auto value = start;
		for (std::size_t i = 0; i < M - cut; i++)
		{
			value = _data[value];
			os << value + 1;
		}
		return os;
	}

	std::ostream& print_formatted(std::ostream& os) const
	{
		auto dist = M - _moves % M;
		const std::size_t init = follow_internal(get_current_internal(), dist);
		std::size_t value = init;
		do {
			if (value == get_current_internal())
				os << "(" << value + 1 << ")";
			else
				os << " " << value + 1 << " ";
			auto next = _data[value];
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
		return cc.print_simple(os, 0, 1);
}

template<std::size_t N>
CrabCups(const char(&data)[N])->CrabCups<N - 1>;

type KnapsackTableProps = {
  dpTable: number[][];
  items: string[];
  capacity: number;
};

export default function KnapsackTable({
  dpTable,
  items,
  capacity,
}: KnapsackTableProps) {
  if (!dpTable.length) return null;

  return (
    <div className="mt-4">
      <h4 className="text-sm font-semibold text-[#17231f] mb-2">
        Tabel DP (0/1 Knapsack)
      </h4>
      <div className="overflow-x-auto">
        <table className="border-collapse text-sm">
          <thead>
            <tr>
              <th className="px-2 py-1 text-[#66746f] font-medium text-xs border border-[#eef5f2]">
                \
              </th>
              {Array.from({ length: capacity + 1 }, (_, j) => (
                <th
                  key={j}
                  className="px-2 py-1 text-[#66746f] font-medium text-xs border border-[#eef5f2]"
                >
                  {j}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {dpTable.map((row, i) => (
              <tr key={i}>
                <td className="px-2 py-1 text-[#66746f] font-medium text-xs border border-[#eef5f2]">
                  {i === 0 ? "0" : items[i - 1] || `item${i}`}
                </td>
                {row.map((val, j) => (
                  <td
                    key={j}
                    className={[
                      "px-3 py-1 border border-[#eef5f2] text-center min-w-[44px]",
                      i === dpTable.length - 1 && j === capacity
                        ? "bg-[#397f70] text-white font-bold"
                        : "",
                    ].join(" ")}
                  >
                    {val.toFixed(2)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-[#66746f] mt-2">
        Baris pertama = tanpa item, kolom pertama = kapasitas 0.
        Nilai akhir (kanan bawah) = total value maksimum.
      </p>
    </div>
  );
}
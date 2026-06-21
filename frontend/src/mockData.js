export const MOCK_TEAMS = {
  mens_football: [
    { id: 'm1', name: 'Khoá 2005' },
    { id: 'm2', name: 'Khoá 2007' },
    { id: 'm3', name: 'Khoá 2008' },
    { id: 'm4', name: 'Khoá 2009' },
    { id: 'm5', name: 'Khoá 2010' },
    { id: 'm6', name: 'Khoá 2011' },
    { id: 'm7', name: 'Khoá 2012' },
    { id: 'm8', name: 'Khoá 2013' },
    { id: 'm9', name: 'Khoá 2014' },
    { id: 'm10', name: 'Khoá 2016' },
    { id: 'm11', name: 'Khoá 2017' },
    { id: 'm12', name: 'Khoá 2018' },
    { id: 'm13', name: 'Khoá 2019' },
    { id: 'm14', name: 'Khoá 2022' },
    { id: 'm15', name: 'Khoá 2023' },
    { id: 'm16', name: 'Khoá 2024' },
    { id: 'm17', name: 'Khoá 2025' },
    { id: 'm18', name: 'Khoá 2026' },
    { id: 'm19', name: 'Trung Tân Đức' },
    { id: 'm20', name: 'Nam Tân Đức' },
    { id: 'm21', name: 'Khối 11' },
  ],
  womens_football: [
    { id: 'w1', name: 'Nữ Khoá 2005' },
    { id: 'w2', name: 'Nữ Khoá 2006' },
    { id: 'w3', name: 'Nữ Khoá 2007' },
    { id: 'w4', name: 'Nữ Khoá 2008' },
    { id: 'w5', name: 'Nữ Khoá 2009' },
    { id: 'w6', name: 'Nữ Khoá 2010' },
    { id: 'w7', name: 'Nữ Khoá 2011' },
    { id: 'w8', name: 'Nữ Khoá 2012' },
  ]
};

export const MOCK_GROUPS = {
  mens_football: [
    { id: 'A', name: 'Bảng A', capacity: 5 },
    { id: 'B', name: 'Bảng B', capacity: 4 },
    { id: 'C', name: 'Bảng C', capacity: 4 },
    { id: 'D', name: 'Bảng D', capacity: 4 },
    { id: 'E', name: 'Bảng E', capacity: 4 },
  ],
  womens_football: [
    { id: 'A', name: 'Bảng A', capacity: 4 },
    { id: 'B', name: 'Bảng B', capacity: 4 },
  ]
};

export const MOCK_SCHEDULE = {
  mens_football: [
    { group: 'A', home: 'A3', away: 'A4', date: '04/07/2026 (T7)', time: '14:30', code: '1' },
    { group: 'A', home: 'A1', away: 'A2', date: '04/07/2026 (T7)', time: '16:00', code: '1' },
    { group: 'B', home: 'B1', away: 'B2', date: '05/07/2026 (CN)', time: '14:30', code: '1' },
    { group: 'B', home: 'B3', away: 'B4', date: '05/07/2026 (CN)', time: '16:00', code: '1' },
    { group: 'A', home: 'A5', away: 'A1', date: '06/07/2026 (T2)', time: '14:30', code: '1.5' },
    { group: 'A', home: 'A2', away: 'A3', date: '06/07/2026 (T2)', time: '16:00', code: '2' },
    { group: 'C', home: 'C3', away: 'C4', date: '07/07/2026 (T3)', time: '14:30', code: '1' },
    { group: 'C', home: 'C1', away: 'C2', date: '07/07/2026 (T3)', time: '16:00', code: '1' },
    { group: 'D', home: 'D3', away: 'D4', date: '09/07/2026 (T5)', time: '14:30', code: '1' },
    { group: 'D', home: 'D1', away: 'D2', date: '09/07/2026 (T5)', time: '16:00', code: '1' },
    { group: 'E', home: 'E3', away: 'E4', date: '10/07/2026 (T6)', time: '14:30', code: '1' },
    { group: 'E', home: 'E1', away: 'E2', date: '10/07/2026 (T6)', time: '16:00', code: '1' },
    { group: 'A', home: 'A1', away: 'A3', date: '11/07/2026 (T7)', time: '14:30', code: '3' },
    { group: 'A', home: 'A4', away: 'A5', date: '11/07/2026 (T7)', time: '16:00', code: '2' },
    { group: 'C', home: 'C3', away: 'C1', date: '12/07/2026 (CN)', time: '14:30', code: '2' },
    { group: 'C', home: 'C4', away: 'C2', date: '12/07/2026 (CN)', time: '16:00', code: '2' },
    { group: 'B', home: 'B4', away: 'B2', date: '13/07/2026 (T2)', time: '14:30', code: '2' },
    { group: 'B', home: 'B3', away: 'B1', date: '13/07/2026 (T2)', time: '16:00', code: '2' },
    { group: 'A', home: 'A5', away: 'A2', date: '14/07/2026 (T3)', time: '14:30', code: '3' },
    { group: 'A', home: 'A4', away: 'A1', date: '14/07/2026 (T3)', time: '16:00', code: '3.5' },
    { group: 'D', home: 'D3', away: 'D1', date: '15/07/2026 (T4)', time: '14:30', code: '2' },
    { group: 'D', home: 'D4', away: 'D2', date: '15/07/2026 (T4)', time: '16:00', code: '2' },
    { group: 'E', home: 'E3', away: 'E1', date: '16/07/2026 (T5)', time: '14:30', code: '2' },
    { group: 'E', home: 'E4', away: 'E2', date: '16/07/2026 (T5)', time: '16:00', code: '2' },
    { group: 'A', home: 'A2', away: 'A4', date: '17/07/2026 (T6)', time: '14:30', code: '4' },
    { group: 'A', home: 'A3', away: 'A5', date: '17/07/2026 (T6)', time: '16:00', code: '4' },
    { group: 'D', home: 'D4', away: 'D1', date: '18/07/2026 (T7)', time: '14:30', code: '3' },
    { group: 'D', home: 'D2', away: 'D3', date: '18/07/2026 (T7)', time: '16:00', code: '3' },
    { group: 'E', home: 'E4', away: 'E1', date: '19/07/2026 (CN)', time: '14:30', code: '3' },
    { group: 'E', home: 'E2', away: 'E3', date: '19/07/2026 (CN)', time: '16:00', code: '3' },
    { group: 'C', home: 'C4', away: 'C1', date: '20/07/2026 (T2)', time: '14:30', code: '3' },
    { group: 'C', home: 'C2', away: 'C3', date: '20/07/2026 (T2)', time: '16:00', code: '3' },
    { group: 'B', home: 'B4', away: 'B1', date: '21/07/2026 (T3)', time: '14:30', code: '3' },
    { group: 'B', home: 'B2', away: 'B3', date: '21/07/2026 (T3)', time: '16:00', code: '3' }
  ],
  womens_football: [
    // Standard round-robin matches for 2 groups of 4 teams
    // Let's mock a simple schedule for women's football just so it does not crash if clicked
    { group: 'A', home: 'A1', away: 'A2', date: '04/07/2026 (T7)', time: '14:30', code: '1' },
    { group: 'A', home: 'A3', away: 'A4', date: '04/07/2026 (T7)', time: '16:00', code: '1' },
    { group: 'B', home: 'B1', away: 'B2', date: '05/07/2026 (CN)', time: '14:30', code: '1' },
    { group: 'B', home: 'B3', away: 'B4', date: '05/07/2026 (CN)', time: '16:00', code: '1' },
    { group: 'A', home: 'A1', away: 'A3', date: '11/07/2026 (T7)', time: '14:30', code: '2' },
    { group: 'A', home: 'A4', away: 'A2', date: '11/07/2026 (T7)', time: '16:00', code: '2' },
    { group: 'B', home: 'B1', away: 'B3', date: '12/07/2026 (CN)', time: '14:30', code: '2' },
    { group: 'B', home: 'B4', away: 'B2', date: '12/07/2026 (CN)', time: '16:00', code: '2' },
    { group: 'A', home: 'A4', away: 'A1', date: '18/07/2026 (T7)', time: '14:30', code: '3' },
    { group: 'A', home: 'A2', away: 'A3', date: '18/07/2026 (T7)', time: '16:00', code: '3' },
    { group: 'B', home: 'B4', away: 'B1', date: '19/07/2026 (CN)', time: '14:30', code: '3' },
    { group: 'B', home: 'B2', away: 'B3', date: '19/07/2026 (CN)', time: '16:00', code: '3' }
  ]
};

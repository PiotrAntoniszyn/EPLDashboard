import React from 'react'
import { render, cleanup, screen } from '@testing-library/react';

import RadarChart from "../RadarChart"


afterEach(() => {
    cleanup()
})

test("testing", () => {
    render(<RadarChart/>)
    const el = screen.getByTestId("radar-instance");
    expect(el).toBeInTheDocument();

})
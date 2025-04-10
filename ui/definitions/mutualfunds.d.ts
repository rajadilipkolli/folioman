export interface MFPortfolio {
  id: number
  name: string
  email: string
  pan: string
}

export interface SchemeCategory {
  main: string
  sub: string
}
export interface Folio {
  folio: String
  invested: number
  units: number
  value: number

  avg_nav: number
}

export interface Scheme {
  id: number
  name: string
  category: SchemeCategory
  nav0: number
  nav1: number
  folios: Array<Folio>
  invested: number
  units: number
  value: number

  avg_nav: number
}

export interface SchemeData {
  [id: string]: Scheme
}

export interface ValueChange {
  D: number
  A: number
}
export interface XIRRValue {
  current: number
  overall: number
}

export interface Summary {
  totalInvested: number
  totalValue: number
  xirr: XIRRValue
  portfolioDate: string
  totalChange: ValueChange
  totalChangePct: ValueChange
}

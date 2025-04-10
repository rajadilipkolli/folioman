// Placeholder for missing definitions. Ensure this file is updated with the correct content.
import { PDFData } from '@/definitions/casparser.d'

export interface StepEvent extends Event {
  pageIndex: number
  pdfData?: PDFData | null
  uploadStatus?: boolean
}

export interface ImportData {
  pdfData: PDFData | null
}

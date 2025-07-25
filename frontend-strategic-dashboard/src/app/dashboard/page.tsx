import { ChartAreaInteractive } from "@/components/chart-area-interactive"
import { ProjectsTable } from "@/components/projects-table"
import { SectionCards } from "@/components/section-cards"

export default function Page() {
  return (
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <SectionCards />
              <div className="px-4 lg:px-6">
                <ChartAreaInteractive />
              </div>
              <div className="px-4 lg:px-6">
                <ProjectsTable />
              </div>
            </div>
  )
}
